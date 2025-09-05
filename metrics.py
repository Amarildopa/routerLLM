#!/usr/bin/env python3
"""
📊 Sistema de Métricas Prometheus para RouterLLM
Monitoramento em tempo real de performance e custos
"""

from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from typing import Dict, Any
import time

class RouterMetrics:
    def __init__(self):
        # Contadores
        self.total_requests = Counter(
            'router_llm_requests_total',
            'Total number of requests processed',
            ['model', 'status']
        )
        
        self.total_tokens = Counter(
            'router_llm_tokens_total',
            'Total tokens processed',
            ['model', 'type']  # type: input/output
        )
        
        self.total_cost = Counter(
            'router_llm_cost_total',
            'Total cost in USD',
            ['model']
        )
        
        # Histogramas
        self.request_duration = Histogram(
            'router_llm_request_duration_seconds',
            'Request duration in seconds',
            ['model'],
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
        )
        
        self.response_time = Histogram(
            'router_llm_response_time_seconds',
            'Response time in seconds',
            ['model'],
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
        )
        
        # Gauges
        self.active_requests = Gauge(
            'router_llm_active_requests',
            'Number of active requests'
        )
        
        self.model_availability = Gauge(
            'router_llm_model_available',
            'Model availability (1=available, 0=unavailable)',
            ['model']
        )
        
        self.cost_per_hour = Gauge(
            'router_llm_cost_per_hour_usd',
            'Cost per hour in USD',
            ['model']
        )
        
        # Métricas customizadas
        self.routing_decisions = Counter(
            'router_llm_routing_decisions_total',
            'Total routing decisions made',
            ['reasoning', 'model_selected']
        )
        
        self.api_errors = Counter(
            'router_llm_api_errors_total',
            'Total API errors',
            ['provider', 'error_type']
        )

    def record_request(self, model: str, status: str = "success"):
        """Registra uma requisição"""
        self.total_requests.labels(model=model, status=status).inc()

    def record_tokens(self, model: str, input_tokens: int, output_tokens: int):
        """Registra tokens processados"""
        self.total_tokens.labels(model=model, type="input").inc(input_tokens)
        self.total_tokens.labels(model=model, type="output").inc(output_tokens)

    def record_cost(self, model: str, cost: float):
        """Registra custo da requisição"""
        self.total_cost.labels(model=model).inc(cost)

    def record_duration(self, model: str, duration: float):
        """Registra duração da requisição"""
        self.request_duration.labels(model=model).observe(duration)

    def record_response_time(self, model: str, response_time: float):
        """Registra tempo de resposta"""
        self.response_time.labels(model=model).observe(response_time)

    def set_active_requests(self, count: int):
        """Define número de requisições ativas"""
        self.active_requests.set(count)

    def set_model_availability(self, model: str, available: bool):
        """Define disponibilidade do modelo"""
        self.model_availability.labels(model=model).set(1 if available else 0)

    def record_routing_decision(self, reasoning: str, model_selected: str):
        """Registra decisão de roteamento"""
        self.routing_decisions.labels(
            reasoning=reasoning, 
            model_selected=model_selected
        ).inc()

    def record_api_error(self, provider: str, error_type: str):
        """Registra erro de API"""
        self.api_errors.labels(provider=provider, error_type=error_type).inc()

    def get_metrics(self) -> str:
        """Retorna métricas no formato Prometheus"""
        return generate_latest()

# Instância global das métricas
metrics = RouterMetrics()
