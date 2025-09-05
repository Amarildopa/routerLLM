#!/usr/bin/env python3
"""
🏠 Teste da Home Page com Chat
"""

import requests
import json

def test_home_page():
    print("🏠 Testando Home Page...")
    
    try:
        # Teste 1: Carregar página inicial
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Home page carrega corretamente")
            
            # Verificar se contém elementos essenciais
            content = response.text
            essential_elements = [
                "RouterLLM Chat",
                "home.js",
                "dashboard.css",
                "Font Awesome",
                "theme-toggle",
                "data-theme"
            ]
            
            for element in essential_elements:
                if element in content:
                    print(f"✅ Contém: {element}")
                else:
                    print(f"❌ Falta: {element}")
        else:
            print(f"❌ Home page retornou status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao carregar home page: {e}")
        return False

def test_chat_functionality():
    print("\n💬 Testando funcionalidade do chat...")
    
    try:
        # Teste de chat via API
        payload = {
            "message": "Olá, teste da home page!",
            "user_id": "test_home"
        }
        
        response = requests.post("http://localhost:8000/chat", json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Chat funcionando!")
            print(f"   Modelo usado: {data.get('model_used', 'N/A')}")
            print(f"   Resposta: {data.get('response', 'N/A')[:100]}...")
            print(f"   Custo: ${data.get('cost_estimate', 0):.6f}")
            print(f"   Tempo: {data.get('response_time', 0):.2f}s")
            return True
        else:
            print(f"❌ Chat retornou status {response.status_code}")
            print(f"   Erro: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste de chat: {e}")
        return False

def test_all_pages():
    print("\n🌐 Testando todas as páginas...")
    
    pages = [
        ("/", "Home Page (Chat)"),
        ("/dashboard", "Dashboard"),
        ("/api-config", "Configuração de APIs"),
        ("/docs", "Documentação Swagger"),
        ("/models", "Lista de Modelos"),
        ("/stats", "Estatísticas")
    ]
    
    for endpoint, description in pages:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}", timeout=5)
            status = "✅" if response.status_code == 200 else "❌"
            print(f"{status} {endpoint} - {description} (Status: {response.status_code})")
        except Exception as e:
            print(f"❌ {endpoint} - {description} (Erro: {e})")

def main():
    print("🚀 Testando Home Page do RouterLLM...")
    print("=" * 50)
    
    # Verificar se o servidor está rodando
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code != 200:
            print("❌ Servidor não está rodando. Execute: py main.py")
            return
    except Exception as e:
        print(f"❌ Não foi possível conectar ao servidor: {e}")
        print("💡 Execute: py main.py")
        return
    
    print("✅ Servidor está rodando!\n")
    
    # Executar testes
    home_ok = test_home_page()
    chat_ok = test_chat_functionality()
    test_all_pages()
    
    # Resumo
    print("\n" + "=" * 50)
    print("📋 RESUMO DOS TESTES:")
    
    if home_ok and chat_ok:
        print("🎉 HOME PAGE FUNCIONANDO PERFEITAMENTE!")
        print("\n🌐 Acesse:")
        print("  - Home (Chat): http://localhost:8000/")
        print("  - Dashboard: http://localhost:8000/dashboard")
        print("  - Configuração: http://localhost:8000/api-config")
        print("  - Documentação: http://localhost:8000/docs")
    else:
        print("⚠️  Alguns problemas foram encontrados. Verifique os logs acima.")

if __name__ == "__main__":
    main()
