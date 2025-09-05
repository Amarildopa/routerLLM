#!/usr/bin/env python3
"""
🧪 Teste de endpoints do RouterLLM
"""

import requests
import json

def test_endpoints():
    base_url = "http://localhost:8000"
    
    print("🔍 Testando endpoints...")
    
    # Teste 1: Página principal
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"✅ GET / - Status: {response.status_code}")
    except Exception as e:
        print(f"❌ GET / - Erro: {e}")
    
    # Teste 2: Dashboard
    try:
        response = requests.get(f"{base_url}/dashboard", timeout=5)
        print(f"✅ GET /dashboard - Status: {response.status_code}")
    except Exception as e:
        print(f"❌ GET /dashboard - Erro: {e}")
    
    # Teste 3: Models
    try:
        response = requests.get(f"{base_url}/models", timeout=5)
        print(f"✅ GET /models - Status: {response.status_code}")
    except Exception as e:
        print(f"❌ GET /models - Erro: {e}")
    
    # Teste 4: Stats
    try:
        response = requests.get(f"{base_url}/stats", timeout=5)
        print(f"✅ GET /stats - Status: {response.status_code}")
    except Exception as e:
        print(f"❌ GET /stats - Erro: {e}")
    
    # Teste 5: Chat (POST)
    try:
        payload = {"message": "Teste"}
        response = requests.post(f"{base_url}/chat", json=payload, timeout=10)
        print(f"✅ POST /chat - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Modelo: {data.get('model_used', 'N/A')}")
        else:
            print(f"   Erro: {response.text}")
    except Exception as e:
        print(f"❌ POST /chat - Erro: {e}")
    
    # Teste 6: Métricas
    try:
        response = requests.get(f"{base_url}/metrics", timeout=5)
        print(f"✅ GET /metrics - Status: {response.status_code}")
    except Exception as e:
        print(f"❌ GET /metrics - Erro: {e}")

if __name__ == "__main__":
    test_endpoints()
