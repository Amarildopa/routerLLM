#!/usr/bin/env python3
"""
🧪 Teste simples da API OpenAI
"""

import requests
import json

def test_openai():
    try:
        print("🔍 Testando API OpenAI...")
        
        # Teste simples
        response = requests.post('http://localhost:8000/chat', 
                               json={'message': 'Olá'}, 
                               timeout=10)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API funcionando!")
            print(f"Modelo usado: {data.get('model_used', 'N/A')}")
            print(f"Resposta: {data.get('response', 'N/A')[:100]}...")
        else:
            print(f"❌ Erro: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_openai()
