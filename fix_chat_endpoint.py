#!/usr/bin/env python3
"""
🔧 Script para corrigir o endpoint /chat
"""

import requests
import subprocess
import time
import sys
import os

def check_server_running():
    """Verifica se o servidor está rodando"""
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        return response.status_code == 200
    except:
        return False

def kill_existing_servers():
    """Mata processos Python existentes"""
    try:
        if os.name == 'nt':  # Windows
            subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                         capture_output=True, text=True)
        else:  # Linux/Mac
            subprocess.run(['pkill', '-f', 'main.py'], 
                         capture_output=True, text=True)
        print("✅ Processos Python anteriores finalizados")
    except Exception as e:
        print(f"⚠️  Erro ao finalizar processos: {e}")

def start_server():
    """Inicia o servidor"""
    try:
        print("🚀 Iniciando RouterLLM...")
        process = subprocess.Popen([sys.executable, 'main.py'], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        return process
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        return None

def test_chat_endpoint():
    """Testa o endpoint /chat"""
    print("🧪 Testando endpoint /chat...")
    
    try:
        # Teste 1: Verificar se o endpoint existe
        response = requests.get("http://localhost:8000/docs")
        if response.status_code == 200:
            print("✅ Documentação Swagger carregada")
        else:
            print(f"❌ Erro na documentação: {response.status_code}")
            return False
        
        # Teste 2: Testar POST /chat
        payload = {"message": "Teste do endpoint"}
        response = requests.post("http://localhost:8000/chat", json=payload, timeout=10)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Endpoint /chat funcionando!")
            print(f"Resposta: {data.get('response', 'N/A')[:100]}...")
            return True
        else:
            print(f"❌ Erro no endpoint /chat: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar endpoint: {e}")
        return False

def main():
    print("🔧 Corrigindo endpoint /chat...")
    print("=" * 50)
    
    # 1. Verificar se o servidor está rodando
    if check_server_running():
        print("✅ Servidor está rodando")
        
        # Testar o endpoint
        if test_chat_endpoint():
            print("🎉 Endpoint /chat já está funcionando!")
            return
        else:
            print("⚠️  Endpoint com problema, reiniciando servidor...")
    else:
        print("❌ Servidor não está rodando")
    
    # 2. Finalizar processos existentes
    kill_existing_servers()
    time.sleep(2)
    
    # 3. Iniciar novo servidor
    process = start_server()
    if not process:
        return
    
    # 4. Aguardar servidor inicializar
    print("⏳ Aguardando servidor inicializar...")
    for i in range(10):
        if check_server_running():
            print("✅ Servidor iniciado!")
            break
        time.sleep(1)
    else:
        print("❌ Servidor não iniciou em 10 segundos")
        return
    
    # 5. Testar o endpoint
    if test_chat_endpoint():
        print("🎉 Endpoint /chat corrigido e funcionando!")
        print("\n🌐 Acesse:")
        print("  - Dashboard: http://localhost:8000/dashboard")
        print("  - API Docs: http://localhost:8000/docs")
        print("  - Configuração: http://localhost:8000/api-config")
    else:
        print("❌ Ainda há problemas com o endpoint /chat")

if __name__ == "__main__":
    main()
