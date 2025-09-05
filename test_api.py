#!/usr/bin/env python3
"""
🧪 Teste da API RouterLLM
Script para testar todas as funcionalidades
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Testa se a API está rodando"""
    print("🔍 Testando health check...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ API está rodando!")
            print(f"📊 Status: {response.json()}")
            return True
        else:
            print(f"❌ API retornou status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return False

def test_models():
    """Testa endpoint de modelos"""
    print("\n🤖 Testando endpoint de modelos...")
    try:
        response = requests.get(f"{BASE_URL}/models")
        if response.status_code == 200:
            data = response.json()
            print("✅ Modelos carregados!")
            print(f"📊 Total: {data['summary']['total']}")
            print(f"🔧 Configurados: {data['summary']['configured']}")
            return True
        else:
            print(f"❌ Erro ao carregar modelos: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_chat(message, force_model=None):
    """Testa endpoint de chat"""
    print(f"\n💬 Testando chat: '{message[:50]}...'")
    
    payload = {"message": message}
    if force_model:
        payload["force_model"] = force_model
        print(f"🔧 Forçando modelo: {force_model}")
    
    try:
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/chat", json=payload)
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Chat funcionando!")
            print(f"🤖 Modelo usado: {data['model_used']}")
            print(f"💭 Reasoning: {data['reasoning']}")
            print(f"💰 Custo: ${data['cost_estimate']:.4f}")
            print(f"⏱️  Tempo: {data['response_time']:.2f}s")
            print(f"📝 Resposta: {data['response'][:100]}...")
            return True
        else:
            print(f"❌ Erro no chat: {response.status_code}")
            print(f"📄 Detalhes: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_stats():
    """Testa endpoint de estatísticas"""
    print("\n📊 Testando estatísticas...")
    try:
        response = requests.get(f"{BASE_URL}/stats")
        if response.status_code == 200:
            data = response.json()
            print("✅ Estatísticas carregadas!")
            print(f"📈 Total de requests: {data['total_requests']}")
            print(f"💰 Custo total: ${data['total_cost']:.4f}")
            print(f"⏱️  Tempo médio: {data['avg_response_time']:.2f}s")
            return True
        else:
            print(f"❌ Erro ao carregar stats: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🚀 Iniciando testes do RouterLLM...")
    
    # Teste 1: Health check
    if not test_health():
        print("\n❌ API não está rodando. Execute: python main.py")
        return
    
    # Teste 2: Modelos
    test_models()
    
    # Teste 3: Chat básico
    test_chat("Olá, como você está?")
    
    # Teste 4: Chat com código
    test_chat("Como fazer um loop em Python?")
    
    # Teste 5: Chat forçando modelo
    test_chat("Teste de modelo específico", "gpt-4o-mini")
    
    # Teste 6: Estatísticas
    test_stats()
    
    print("\n🎉 Testes concluídos!")

if __name__ == "__main__":
    main()

