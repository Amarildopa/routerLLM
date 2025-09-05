#!/usr/bin/env python3
"""
🧪 Teste simples do endpoint /chat
"""

import requests
import json

def test_chat_simple():
    print("🧪 Testando endpoint /chat...")
    
    # URL do endpoint
    url = "http://localhost:8000/chat"
    
    # Payload de teste
    payload = {
        "message": "Olá, teste simples"
    }
    
    # Headers
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print(f"📡 Enviando POST para: {url}")
        print(f"📦 Payload: {json.dumps(payload, indent=2)}")
        
        # Fazer a requisição
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCESSO!")
            print(f"📝 Resposta: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print("❌ ERRO!")
            print(f"📝 Resposta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão - Servidor não está rodando")
        print("💡 Execute: py main.py")
    except requests.exceptions.Timeout:
        print("❌ Timeout - Servidor demorou para responder")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

def test_other_endpoints():
    print("\n🔍 Testando outros endpoints...")
    
    endpoints = [
        ("GET", "/", "Página principal"),
        ("GET", "/docs", "Documentação Swagger"),
        ("GET", "/models", "Lista de modelos"),
        ("GET", "/stats", "Estatísticas"),
        ("GET", "/dashboard", "Dashboard"),
        ("GET", "/api-config", "Configuração de APIs")
    ]
    
    for method, endpoint, description in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"http://localhost:8000{endpoint}", timeout=5)
            else:
                response = requests.post(f"http://localhost:8000{endpoint}", timeout=5)
            
            status = "✅" if response.status_code == 200 else "❌"
            print(f"{status} {method} {endpoint} - {description} (Status: {response.status_code})")
            
        except Exception as e:
            print(f"❌ {method} {endpoint} - {description} (Erro: {e})")

if __name__ == "__main__":
    test_chat_simple()
    test_other_endpoints()
