#!/usr/bin/env python3
"""
🧪 Teste direto da API OpenAI
"""

import os
import httpx
import asyncio
from dotenv import load_dotenv

async def test_openai_direct():
    print("🔍 Testando chave da OpenAI diretamente...")
    
    # Carregar variáveis de ambiente
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ Chave da OpenAI não encontrada no .env")
        return
    
    print(f"✅ Chave encontrada: {api_key[:10]}...{api_key[-4:]}")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": "Olá, teste"}],
        "max_tokens": 50,
        "temperature": 0.7
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Chave da OpenAI funcionando!")
            print(f"Resposta: {data['choices'][0]['message']['content']}")
        else:
            print(f"❌ Erro da OpenAI: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")

if __name__ == "__main__":
    asyncio.run(test_openai_direct())
