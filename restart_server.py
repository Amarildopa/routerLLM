#!/usr/bin/env python3
"""
🔄 Script para reiniciar o servidor RouterLLM
"""

import subprocess
import time
import requests
import os
import signal
import sys

def kill_existing_server():
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

def test_server():
    """Testa se o servidor está funcionando"""
    for i in range(10):  # Tentar por 10 segundos
        try:
            response = requests.get('http://localhost:8000/', timeout=2)
            if response.status_code == 200:
                print("✅ Servidor funcionando!")
                return True
        except:
            pass
        time.sleep(1)
    return False

def main():
    print("🔄 Reiniciando RouterLLM...")
    
    # 1. Finalizar processos existentes
    kill_existing_server()
    time.sleep(2)
    
    # 2. Iniciar novo servidor
    process = start_server()
    if not process:
        return
    
    # 3. Testar se está funcionando
    if test_server():
        print("🎉 Servidor reiniciado com sucesso!")
        print("🌐 Dashboard: http://localhost:8000/dashboard")
        print("📚 API Docs: http://localhost:8000/docs")
        
        # Manter o processo rodando
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Parando servidor...")
            process.terminate()
    else:
        print("❌ Servidor não iniciou corretamente")
        process.terminate()

if __name__ == "__main__":
    main()
