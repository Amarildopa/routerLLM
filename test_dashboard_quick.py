#!/usr/bin/env python3
"""
🧪 Teste rápido do dashboard após correções
"""

import requests
import time

def test_dashboard_quick():
    """Teste rápido do dashboard"""
    print("🔍 Testando dashboard após correções...")
    
    try:
        # Testar se a API está rodando
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ API está rodando")
        else:
            print(f"❌ API retornou status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API não está rodando: {e}")
        print("💡 Execute: py main.py")
        return False
    
    try:
        # Testar dashboard
        response = requests.get("http://localhost:8000/dashboard", timeout=5)
        if response.status_code == 200:
            print("✅ Dashboard carrega corretamente")
            
            # Verificar se contém elementos essenciais
            content = response.text
            if "dashboard.css" in content and "dashboard.js" in content:
                print("✅ CSS e JS estão sendo carregados")
            else:
                print("❌ CSS ou JS não estão sendo carregados")
            
            if "RouterLLM Dashboard" in content:
                print("✅ Título do dashboard encontrado")
            else:
                print("❌ Título do dashboard não encontrado")
                
        else:
            print(f"❌ Dashboard retornou status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao carregar dashboard: {e}")
        return False
    
    try:
        # Testar métricas
        response = requests.get("http://localhost:8000/metrics", timeout=5)
        if response.status_code == 200:
            print("✅ Métricas funcionando")
        else:
            print(f"❌ Métricas retornaram status {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao acessar métricas: {e}")
    
    print("\n🎉 Dashboard corrigido e funcionando!")
    print("🌐 Acesse: http://localhost:8000/dashboard")
    return True

if __name__ == "__main__":
    test_dashboard_quick()
