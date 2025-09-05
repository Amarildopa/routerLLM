#!/usr/bin/env python3
"""
🔍 Verificar configuração do .env
"""

import os
from dotenv import load_dotenv

def check_env():
    print("🔍 Verificando configuração do .env...")
    
    # Carregar variáveis de ambiente
    load_dotenv()
    
    # Verificar chaves
    openai_key = os.getenv('OPENAI_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    google_key = os.getenv('GOOGLE_API_KEY')
    
    print(f"OpenAI API Key: {'✅ Configurada' if openai_key else '❌ Não configurada'}")
    if openai_key:
        print(f"  Valor: {openai_key[:10]}...{openai_key[-4:] if len(openai_key) > 14 else 'muito curta'}")
    
    print(f"Anthropic API Key: {'✅ Configurada' if anthropic_key else '❌ Não configurada'}")
    print(f"Google API Key: {'✅ Configurada' if google_key else '❌ Não configurada'}")
    
    # Verificar se a chave da OpenAI é válida
    if openai_key:
        if openai_key.startswith('sk-'):
            print("✅ Formato da chave OpenAI parece correto")
        else:
            print("❌ Formato da chave OpenAI incorreto (deve começar com 'sk-')")
        
        if len(openai_key) > 20:
            print("✅ Tamanho da chave OpenAI parece correto")
        else:
            print("❌ Chave OpenAI muito curta")

if __name__ == "__main__":
    check_env()
