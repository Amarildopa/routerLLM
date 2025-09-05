#!/usr/bin/env python3
"""
🚀 RouterLLM - Seu Roteador Inteligente de Modelos
Criado para otimizar custo e performance automaticamente
"""

from fastapi import FastAPI, HTTPException
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

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RouterLLM - Seu Roteador Inteligente",
    description="Roteador que escolhe o melhor modelo LLM para cada tarefa",
    version="1.0.0"
)

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

@app.get("/")
async def root():
    available_models_config = config.get_available_models()
    configured_count = len(available_models_config)
    
    return {
        "message": "🚀 RouterLLM está rodando!",
        "version": "1.0.0",
        "models_configured": configured_count,
        "total_models": len(config.models),
        "available_models": list(available_models_config.keys()),
        "available_providers": config.available_providers,
        "default_model": config.default_model,
        "status": "online" if configured_count > 0 else "waiting_for_api_keys",
        "documentation": "/docs"
    }

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

        # Log da transação
        logger.info(f"User: {request.user_id} | Model: {selected_model} | Tokens: {tokens_used} | Cost: ${cost_estimate:.4f}")

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

if __name__ == "__main__":
    print("🚀 Iniciando RouterLLM...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
