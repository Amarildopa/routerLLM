#!/usr/bin/env python3
"""
🚀 RouterLLM - Seu Roteador Inteligente de Modelos
Criado para otimizar custo e performance automaticamente
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
import asyncio
import httpx
import time
import logging
import os
from datetime import datetime
from dotenv import load_dotenv

from router import LLMRouter
from config import RouterConfig
from metrics import metrics

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Setup logging
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('router_llm.log')
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RouterLLM - Seu Roteador Inteligente",
    description="Roteador que escolhe o melhor modelo LLM para cada tarefa",
    version="1.0.0"
)

# Configurar arquivos estáticos e templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Inicializar o roteador
config = RouterConfig()
router = LLMRouter(config)

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = "anonymous"
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7
    force_model: Optional[str] = None  # Para forçar um modelo específico

class ChatResponse(BaseModel):
    response: str
    model_used: str
    reasoning: str
    cost_estimate: float
    response_time: float
    tokens_used: int

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    available_models_config = config.get_available_models()
    configured_count = len(available_models_config)
    
    return templates.TemplateResponse("home.html", {
        "request": request,
        "message": "🚀 RouterLLM está rodando!",
        "version": "1.0.0",
        "models_configured": configured_count,
        "total_models": len(config.models),
        "available_models": list(available_models_config.keys()),
        "available_providers": config.available_providers,
        "default_model": config.default_model,
        "status": "online" if configured_count > 0 else "waiting_for_api_keys",
        "documentation": "/docs"
    })

@app.get("/models")
async def get_models():
    """Lista todos os modelos disponíveis e suas características"""
    available_models_config = config.get_available_models()
    
    models_with_status = {}
    for model_name, model_config in config.models.items():
        is_available = model_name in available_models_config
        models_with_status[model_name] = {
            **model_config,
            "available": is_available,
            "status": "✅ Configurado" if is_available else "❌ Chave de API necessária"
        }
    
    missing_models = [model for model in config.models.keys() if model not in available_models_config]
    
    return {
        "models": models_with_status,
        "summary": {
            "total": len(config.models),
            "configured": len(available_models_config),
            "missing_keys": missing_models,
            "available_providers": config.available_providers
        }
    }

@app.get("/status")
async def get_api_status():
    """Verifica o status das chaves de API configuradas usando a configuração flexível"""
    
    # Usar a configuração flexível para detectar providers
    all_providers = ["openai", "anthropic", "google"]
    api_status = {}
    
    for provider in all_providers:
        # Obter modelos deste provider
        provider_models = [model for model, config_data in config.models.items() 
                          if config_data["provider"] == provider]
        
        api_status[provider] = {
            "configured": config.is_provider_available(provider),
            "models": provider_models,
            "env_var": f"{provider.upper()}_API_KEY"
        }
    
    configured_providers = config.available_providers
    
    return {
        "providers": api_status,
        "summary": {
            "total_providers": len(api_status),
            "configured_providers": len(configured_providers),
            "ready_to_use": len(configured_providers) > 0,
            "next_steps": "Configure pelo menos uma chave de API no arquivo .env" if len(configured_providers) == 0 else "Pronto para usar!"
        }
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Endpoint principal para chat com roteamento inteligente"""
    start_time = time.time()

    try:
        # Escolher o modelo baseado na entrada
        if request.force_model:
            selected_model = request.force_model
            reasoning = f"Modelo forçado pelo usuário: {request.force_model}"
        else:
            selected_model, reasoning = router.route_request(
                message=request.message,
                user_id=request.user_id
            )

        # Fazer a chamada para o modelo escolhido
        response_text, tokens_used = await router.call_model(
            model=selected_model,
            message=request.message,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )

        # Calcular métricas
        response_time = time.time() - start_time
        cost_estimate = router.calculate_cost(selected_model, tokens_used)

        # Registrar métricas
        metrics.record_request(selected_model, "success")
        metrics.record_tokens(selected_model, len(request.message.split()), len(response_text.split()))
        metrics.record_cost(selected_model, cost_estimate)
        metrics.record_duration(selected_model, response_time)
        metrics.record_response_time(selected_model, response_time)
        metrics.record_routing_decision(reasoning, selected_model)

        # Log da transação
        logger.info(f"✅ Request completed | User: {request.user_id} | Model: {selected_model} | Tokens: {tokens_used} | Cost: ${cost_estimate:.4f} | Time: {response_time:.2f}s")

        return ChatResponse(
            response=response_text,
            model_used=selected_model,
            reasoning=reasoning,
            cost_estimate=cost_estimate,
            response_time=response_time,
            tokens_used=tokens_used
        )

    except Exception as e:
        logger.error(f"Erro no chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/stats")
async def get_stats():
    """Estatísticas de uso do roteador"""
    return router.get_stats()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Página inicial com chat integrado"""
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard web do RouterLLM"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/metrics")
async def get_metrics():
    """Endpoint de métricas para Prometheus"""
    return Response(metrics.get_metrics(), media_type=CONTENT_TYPE_LATEST)

@app.get("/api-config", response_class=HTMLResponse)
async def api_config(request: Request):
    """Tela de configuração de APIs"""
    return templates.TemplateResponse("api_config.html", {"request": request})

@app.get("/api-config/status")
async def get_api_status_config():
    """Status das APIs para configuração"""
    openai_key = os.getenv("OPENAI_API_KEY", "")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
    google_key = os.getenv("GOOGLE_API_KEY", "")
    
    return {
        "openai": {
            "available": bool(openai_key and openai_key.strip() and not openai_key.startswith('sk-...')),
            "key": openai_key[:10] + "..." + openai_key[-4:] if openai_key else None
        },
        "anthropic": {
            "available": bool(anthropic_key and anthropic_key.strip() and not anthropic_key.startswith('sk-ant-...')),
            "key": anthropic_key[:10] + "..." + anthropic_key[-4:] if anthropic_key else None
        },
        "google": {
            "available": bool(google_key and google_key.strip() and google_key != '...'),
            "key": google_key[:10] + "..." + google_key[-4:] if google_key else None
        }
    }

@app.post("/api-config/test")
async def test_api_key(request: dict):
    """Testa uma chave de API"""
    provider = request.get("provider")
    api_key = request.get("api_key")
    
    if not provider or not api_key:
        return {"success": False, "error": "Provider e API key são obrigatórios"}
    
    try:
        if provider == "openai":
            # Teste simples da OpenAI
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            payload = {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": "test"}], "max_tokens": 5}
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            
            if response.status_code == 200:
                return {"success": True, "message": "Chave OpenAI válida"}
            else:
                return {"success": False, "error": f"Erro OpenAI: {response.status_code}"}
                
        elif provider == "anthropic":
            # Teste simples da Anthropic
            headers = {"x-api-key": api_key, "Content-Type": "application/json", "anthropic-version": "2023-06-01"}
            payload = {"model": "claude-3-haiku-20240307", "max_tokens": 5, "messages": [{"role": "user", "content": "test"}]}
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload)
            
            if response.status_code == 200:
                return {"success": True, "message": "Chave Anthropic válida"}
            else:
                return {"success": False, "error": f"Erro Anthropic: {response.status_code}"}
                
        elif provider == "google":
            # Teste simples do Google
            payload = {"contents": [{"parts": [{"text": "test"}]}], "generationConfig": {"maxOutputTokens": 5}}
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={api_key}", json=payload)
            
            if response.status_code == 200:
                return {"success": True, "message": "Chave Google válida"}
            else:
                return {"success": False, "error": f"Erro Google: {response.status_code}"}
        else:
            return {"success": False, "error": "Provider não suportado"}
            
    except Exception as e:
        return {"success": False, "error": f"Erro de conexão: {str(e)}"}

@app.post("/api-config/save")
async def save_api_key(request: dict):
    """Salva uma chave de API (simulação - em produção, salvaria no .env)"""
    provider = request.get("provider")
    api_key = request.get("api_key")
    
    if not provider or not api_key:
        return {"success": False, "error": "Provider e API key são obrigatórios"}
    
    # Em produção, aqui você salvaria no arquivo .env
    # Por enquanto, apenas simulamos o sucesso
    logger.info(f"Chave {provider} salva: {api_key[:10]}...")
    
    return {
        "success": True, 
        "message": f"Chave {provider.upper()} salva com sucesso!",
        "note": "Em produção, a chave seria salva no arquivo .env"
    }

@app.post("/api-config/save-all")
async def save_all_api_keys(request: dict):
    """Salva todas as chaves de API"""
    keys = request
    
    if not keys:
        return {"success": False, "error": "Nenhuma chave fornecida"}
    
    saved_count = 0
    for provider, key in keys.items():
        if key and key.strip():
            logger.info(f"Chave {provider} salva: {key[:10]}...")
            saved_count += 1
    
    return {
        "success": True,
        "message": f"{saved_count} chaves salvas com sucesso!",
        "saved_count": saved_count,
        "note": "Em produção, as chaves seriam salvas no arquivo .env"
    }

if __name__ == "__main__":
    print("🚀 Iniciando RouterLLM...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
