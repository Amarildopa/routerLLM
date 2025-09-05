#!/usr/bin/env python3
"""
🧠 Lógica principal do RouterLLM
Aqui acontece a mágica do roteamento inteligente
"""

import re
import httpx
import asyncio
import os
from typing import Tuple, Dict, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class LLMRouter:
    def __init__(self, config):
        self.config = config
        self.stats = {
            "total_requests": 0,
            "model_usage": {},
            "total_cost": 0.0,
            "avg_response_time": 0.0
        }

    def get_available_models(self) -> Dict[str, bool]:
        """
        🔍 Verifica quais modelos estão disponíveis baseado nas chaves de API
        Usa a nova configuração flexível
        """
        available_models_config = self.config.get_available_models()
        available = {}
        
        for model_name in self.config.models.keys():
            available[model_name] = model_name in available_models_config
        
        return available

    def route_request(self, message: str, user_id: str = "anonymous") -> Tuple[str, str]:
        """
        🎯 Coração do roteador - decide qual modelo usar com fallback inteligente
        Agora usa configuração flexível baseada nas APIs disponíveis
        """
        message_lower = message.lower()
        message_length = len(message)
        available_models_config = self.config.get_available_models()
        
        # Se nenhum modelo disponível, retorna erro
        if not available_models_config:
            return "error", "❌ Nenhuma API configurada. Configure pelo menos uma chave de API no arquivo .env"
        
        # Lista de preferências por categoria
        preferred_models = []
        reasoning = ""

        # Filtrar apenas modelos disponíveis para as preferências
        available_model_names = list(available_models_config.keys())
        
        # Regra 1: Código/Programação → Modelo premium
        code_keywords = ['código', 'code', 'python', 'javascript', 'sql', 'debug', 'erro', 'função', 'class', 'import']
        if any(keyword in message_lower for keyword in code_keywords):
            all_preferred = ["gpt-4", "claude-3-5-sonnet", "gpt-4o-mini"]
            preferred_models = [m for m in all_preferred if m in available_model_names]
            reasoning = "🔧 Detectei programação - priorizando modelos premium"

        # Regra 2: Perguntas curtas e simples → Modelo econômico
        elif message_length < 100:
            simple_patterns = ['o que é', 'como', 'quando', 'onde', 'quem', 'sim ou não', 'verdadeiro ou falso']
            if any(pattern in message_lower for pattern in simple_patterns):
                all_preferred = ["gpt-4o-mini", "claude-3-haiku", "gpt-4"]
                preferred_models = [m for m in all_preferred if m in available_model_names]
                reasoning = "⚡ Pergunta simples - priorizando modelos rápidos"

        # Regra 3: Textos longos/análises → Modelo com contexto grande
        elif message_length > 1000:
            all_preferred = ["claude-3-5-sonnet", "gemini-1.5-pro", "gpt-4"]
            preferred_models = [m for m in all_preferred if m in available_model_names]
            reasoning = "📄 Texto longo - priorizando modelos com contexto extenso"

        # Regra 4: Criatividade/Marketing → Modelo criativo
        elif any(keyword in message_lower for keyword in ['criativo', 'marketing', 'copy', 'slogan', 'história', 'poema', 'roteiro']):
            all_preferred = ["gemini-1.5-pro", "claude-3-5-sonnet", "gpt-4"]
            preferred_models = [m for m in all_preferred if m in available_model_names]
            reasoning = "🎨 Conteúdo criativo - priorizando modelos criativos"

        # Regra 5: Padrão → Modelo balanceado
        else:
            all_preferred = ["claude-3-haiku", "gpt-4o-mini", "gpt-4"]
            preferred_models = [m for m in all_preferred if m in available_model_names]
            reasoning = "⚖️ Caso geral - priorizando modelos balanceados"

        # Escolher o primeiro modelo disponível da lista de preferências
        if preferred_models:
            selected_model = preferred_models[0]
            return selected_model, f"{reasoning} (usando {selected_model})"
        
        # Fallback: usar o modelo padrão da configuração
        default_model = self.config.default_model
        if default_model in available_model_names:
            return default_model, f"⚠️ Usando {default_model} (modelo padrão)"
        
        # Último fallback: usar qualquer modelo disponível
        if available_model_names:
            fallback_model = available_model_names[0]
            return fallback_model, f"⚠️ Usando {fallback_model} (único modelo disponível)"
        
        # Se nenhum modelo disponível (não deveria chegar aqui devido à verificação anterior)
        return "error", "❌ Nenhuma chave de API configurada! Configure pelo menos uma chave no arquivo .env"

    async def call_model(self, model: str, message: str, max_tokens: int = 1000, temperature: float = 0.7) -> Tuple[str, int]:
        """
        📡 Faz a chamada real para o modelo escolhido
        """
        model_config = self.config.models.get(model)
        if not model_config:
            raise ValueError(f"Modelo {model} não configurado")

        provider = model_config["provider"]
        
        try:
            if provider == "openai":
                response_text, tokens_used = await self._call_openai(model, message, max_tokens, temperature)
            elif provider == "anthropic":
                response_text, tokens_used = await self._call_anthropic(model, message, max_tokens, temperature)
            elif provider == "google":
                response_text, tokens_used = await self._call_google(model, message, max_tokens, temperature)
            else:
                raise ValueError(f"Provider {provider} não implementado")
                
        except Exception as e:
            logger.error(f"Erro ao chamar {model}: {e}")
            # Fallback para simulação em caso de erro
            await asyncio.sleep(0.5)
            response_text = f"⚠️ [ERRO] Não foi possível conectar com {model}. Verifique sua chave de API."
            tokens_used = len(message.split()) * 2

        # Atualizar estatísticas
        self.stats["total_requests"] += 1
        self.stats["model_usage"][model] = self.stats["model_usage"].get(model, 0) + 1

        return response_text, tokens_used

    async def _call_openai(self, model: str, message: str, max_tokens: int, temperature: float) -> Tuple[str, int]:
        """
        🤖 Chama a API da OpenAI
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "sk-...":
            raise ValueError("Chave da OpenAI não configurada")
            
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Mapear modelo para nome da API
        api_model = "gpt-4" if model == "gpt-4" else "gpt-4o-mini"
        
        payload = {
            "model": api_model,
            "messages": [{"role": "user", "content": message}],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
        if response.status_code != 200:
            raise Exception(f"OpenAI API erro {response.status_code}: {response.text}")
            
        data = response.json()
        response_text = data["choices"][0]["message"]["content"]
        tokens_used = data["usage"]["total_tokens"]
        
        return response_text, tokens_used

    async def _call_anthropic(self, model: str, message: str, max_tokens: int, temperature: float) -> Tuple[str, int]:
        """
        🧠 Chama a API da Anthropic (Claude)
        """
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key or api_key == "sk-ant-...":
            raise ValueError("Chave da Anthropic não configurada")
            
        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        # Mapear modelo para nome da API
        api_model = "claude-3-haiku-20240307" if model == "claude-3-haiku" else "claude-3-5-sonnet-20241022"
        
        payload = {
            "model": api_model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": message}]
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload
            )
            
        if response.status_code != 200:
            raise Exception(f"Anthropic API erro {response.status_code}: {response.text}")
            
        data = response.json()
        response_text = data["content"][0]["text"]
        tokens_used = data["usage"]["input_tokens"] + data["usage"]["output_tokens"]
        
        return response_text, tokens_used

    async def _call_google(self, model: str, message: str, max_tokens: int, temperature: float) -> Tuple[str, int]:
        """
        🌟 Chama a API do Google (Gemini)
        """
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key or api_key == "...":
            raise ValueError("Chave do Google não configurada")
            
        headers = {
            "Content-Type": "application/json"
        }
        
        # Mapear modelo para nome da API
        api_model = "gemini-1.5-pro"
        
        payload = {
            "contents": [{
                "parts": [{"text": message}]
            }],
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": temperature
            }
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{api_model}:generateContent?key={api_key}",
                headers=headers,
                json=payload
            )
            
        if response.status_code != 200:
            raise Exception(f"Google API erro {response.status_code}: {response.text}")
            
        data = response.json()
        response_text = data["candidates"][0]["content"]["parts"][0]["text"]
        # Estimativa de tokens (Google não retorna contagem exata)
        tokens_used = len(message.split()) + len(response_text.split())
        
        return response_text, tokens_used

    def calculate_cost(self, model: str, tokens_used: int) -> float:
        """💰 Calcula o custo estimado da chamada"""
        model_config = self.config.models.get(model, {})
        cost_per_1k = model_config.get("cost_per_1k_tokens", 0.001)
        return (tokens_used / 1000) * cost_per_1k

    def get_stats(self) -> Dict[str, Any]:
        """📊 Retorna estatísticas de uso"""
        return {
            **self.stats,
            "timestamp": datetime.now().isoformat(),
            "most_used_model": max(self.stats["model_usage"], key=self.stats["model_usage"].get) if self.stats["model_usage"] else None
        }
