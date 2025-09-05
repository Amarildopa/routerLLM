#!/usr/bin/env python3
"""
🧪 Teste específico do Dashboard RouterLLM
Valida todas as funcionalidades do dashboard web
"""

import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"

def test_dashboard_endpoints():
    """Testa todos os endpoints do dashboard"""
    print("🔍 Testando endpoints do dashboard...")
    
    endpoints = [
        ("/", "Página principal"),
        ("/dashboard", "Dashboard web"),
        ("/models", "Lista de modelos"),
        ("/stats", "Estatísticas"),
        ("/metrics", "Métricas Prometheus"),
        ("/docs", "Documentação Swagger")
    ]
    
    results = []
    
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
            status = "✅" if response.status_code == 200 else "❌"
            print(f"{status} {description}: {response.status_code}")
            results.append((endpoint, response.status_code == 200))
        except Exception as e:
            print(f"❌ {description}: Erro - {e}")
            results.append((endpoint, False))
    
    return results

def test_dashboard_functionality():
    """Testa funcionalidades específicas do dashboard"""
    print("\n🎯 Testando funcionalidades do dashboard...")
    
    # Teste 1: Verificar se o dashboard carrega
    try:
        response = requests.get(f"{BASE_URL}/dashboard", timeout=5)
        if response.status_code == 200:
            print("✅ Dashboard carrega corretamente")
            
            # Verificar se contém elementos essenciais
            content = response.text
            essential_elements = [
                "RouterLLM Dashboard",
                "dashboard.css",
                "dashboard.js",
                "Chart.js",
                "Font Awesome"
            ]
            
            for element in essential_elements:
                if element in content:
                    print(f"✅ Contém: {element}")
                else:
                    print(f"❌ Falta: {element}")
        else:
            print(f"❌ Dashboard retornou status {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao carregar dashboard: {e}")

def test_metrics_endpoint():
    """Testa endpoint de métricas Prometheus"""
    print("\n📊 Testando métricas Prometheus...")
    
    try:
        response = requests.get(f"{BASE_URL}/metrics", timeout=5)
        if response.status_code == 200:
            print("✅ Endpoint de métricas funcionando")
            
            # Verificar se contém métricas esperadas
            content = response.text
            expected_metrics = [
                "router_llm_requests_total",
                "router_llm_tokens_total",
                "router_llm_cost_total",
                "router_llm_request_duration_seconds"
            ]
            
            for metric in expected_metrics:
                if metric in content:
                    print(f"✅ Métrica encontrada: {metric}")
                else:
                    print(f"⚠️  Métrica não encontrada: {metric}")
        else:
            print(f"❌ Métricas retornaram status {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao acessar métricas: {e}")

def test_chat_integration():
    """Testa integração do chat com métricas"""
    print("\n💬 Testando integração chat + métricas...")
    
    try:
        # Fazer uma requisição de teste
        payload = {
            "message": "Teste do dashboard",
            "user_id": "test_user"
        }
        
        response = requests.post(f"{BASE_URL}/chat", json=payload, timeout=10)
        if response.status_code == 200:
            print("✅ Chat funcionando")
            
            # Verificar se as métricas foram atualizadas
            metrics_response = requests.get(f"{BASE_URL}/metrics", timeout=5)
            if metrics_response.status_code == 200:
                metrics_content = metrics_response.text
                if "router_llm_requests_total" in metrics_content:
                    print("✅ Métricas atualizadas após chat")
                else:
                    print("⚠️  Métricas não foram atualizadas")
        else:
            print(f"❌ Chat retornou status {response.status_code}")
    except Exception as e:
        print(f"❌ Erro no teste de chat: {e}")

def main():
    """Executa todos os testes do dashboard"""
    print("🚀 Iniciando validação completa do Dashboard RouterLLM...")
    print("=" * 60)
    
    # Verificar se a API está rodando
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code != 200:
            print("❌ API não está rodando. Execute: py main.py")
            return
    except Exception as e:
        print(f"❌ Não foi possível conectar à API: {e}")
        print("💡 Execute: py main.py")
        return
    
    print("✅ API está rodando!\n")
    
    # Executar testes
    endpoint_results = test_dashboard_endpoints()
    test_dashboard_functionality()
    test_metrics_endpoint()
    test_chat_integration()
    
    # Resumo
    print("\n" + "=" * 60)
    print("📋 RESUMO DA VALIDAÇÃO:")
    
    successful_endpoints = sum(1 for _, success in endpoint_results if success)
    total_endpoints = len(endpoint_results)
    
    print(f"✅ Endpoints funcionando: {successful_endpoints}/{total_endpoints}")
    
    if successful_endpoints == total_endpoints:
        print("🎉 DASHBOARD VALIDADO COM SUCESSO!")
        print("\n🌐 Acesse o dashboard em: http://localhost:8000/dashboard")
        print("📊 Métricas em: http://localhost:8000/metrics")
        print("📚 Documentação em: http://localhost:8000/docs")
    else:
        print("⚠️  Alguns problemas foram encontrados. Verifique os logs acima.")

if __name__ == "__main__":
    main()
