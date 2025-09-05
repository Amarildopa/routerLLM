#!/usr/bin/env python3
"""
⚙️ Configurações do RouterLLM
Aqui você define modelos, custos e regras
"""

import os
from typing import Dict, List, Optional

class RouterConfig:
    def __init__(self):
        # 🔑 Detectar APIs disponíveis baseado nas chaves configuradas
        self.available_providers = self._detect_available_providers()
        # 🤖 Modelos disponíveis e suas características
        self.models = {
            "gpt-4o-mini": {
                "provider": "openai",
                "cost_per_1k_tokens": 0.00015,
                "max_tokens": 16000,
                "speed": "fast",
                "quality": "good",
                "use_case": "Perguntas simples, respostas rápidas"
            },
            "gpt-4": {
                "provider": "openai", 
                "cost_per_1k_tokens": 0.03,
                "max_tokens": 8000,
                "speed": "medium",
                "quality": "excellent",
                "use_case": "Código, raciocínio complexo, precisão"
            },
            "claude-3-haiku": {
                "provider": "anthropic",
                "cost_per_1k_tokens": 0.00025,
                "max_tokens": 200000,
                "speed": "fast",
                "quality": "very_good",
                "use_case": "Balanceado - boa qualidade, bom preço"
            },
            "claude-3-5-sonnet": {
                "provider": "anthropic",
                "cost_per_1k_tokens": 0.003,
                "max_tokens": 200000,
                "speed": "medium",
                "quality": "excellent",
                "use_case": "Textos longos, análises profundas"
            },
            "gemini-1.5-pro": {
                "provider": "google",
                "cost_per_1k_tokens": 0.00125,
                "max_tokens": 1000000,
                "speed": "medium",
                "quality": "excellent",
                "use_case": "Criatividade, contexto gigante"
            }
        }

        # 🎯 Regras de roteamento (para referência)
        self.routing_rules = {
            "code_detection": ["código", "code", "python", "javascript", "debug"],
            "simple_questions": ["o que é", "como", "quando", "onde"],
            "creative_content": ["criativo", "marketing", "história", "poema"],
            "long_text_threshold": 1000,
            "simple_text_threshold": 100
        }

        # 🔧 Configurações gerais (dinâmicas baseadas nas APIs disponíveis)
        self.default_model = self._get_default_model()
        self.fallback_model = self._get_fallback_model()
        self.max_retries = 3
        self.timeout_seconds = 30
    
    def _detect_available_providers(self) -> List[str]:
        """Detecta quais provedores estão disponíveis baseado nas chaves de API"""
        providers = []
        
        # Verifica OpenAI
        if os.getenv('OPENAI_API_KEY'):
            providers.append('openai')
        
        # Verifica Anthropic
        if os.getenv('ANTHROPIC_API_KEY'):
            providers.append('anthropic')
        
        # Verifica Google
        if os.getenv('GOOGLE_API_KEY'):
            providers.append('google')
        
        return providers
    
    def _get_default_model(self) -> str:
        """Retorna o modelo padrão baseado nas APIs disponíveis"""
        # Prioridade: Anthropic > OpenAI > Google
        if 'anthropic' in self.available_providers:
            return 'claude-3-haiku'
        elif 'openai' in self.available_providers:
            return 'gpt-4o-mini'
        elif 'google' in self.available_providers:
            return 'gemini-1.5-pro'
        else:
            # Se nenhuma API disponível, retorna o primeiro modelo (será tratado como erro)
            return 'gpt-4o-mini'
    
    def _get_fallback_model(self) -> str:
        """Retorna o modelo de fallback baseado nas APIs disponíveis"""
        # Se OpenAI disponível, usa como fallback
        if 'openai' in self.available_providers:
            return 'gpt-4o-mini'
        # Senão, usa o mesmo que o padrão
        return self.default_model
    
    def get_available_models(self) -> Dict[str, dict]:
        """Retorna apenas os modelos dos provedores disponíveis"""
        available_models = {}
        for model_name, model_config in self.models.items():
            if model_config['provider'] in self.available_providers:
                available_models[model_name] = model_config
        return available_models
    
    def is_provider_available(self, provider: str) -> bool:
        """Verifica se um provedor específico está disponível"""
        return provider in self.available_providers
