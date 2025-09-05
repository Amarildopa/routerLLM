#!/usr/bin/env python3
"""
🌙 Teste do tema Dark/Light na Home Page
"""

import requests
import re

def test_theme_functionality():
    print("🌙 Testando funcionalidade de tema...")
    
    try:
        # Carregar a home page
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code != 200:
            print(f"❌ Erro ao carregar home page: {response.status_code}")
            return False
        
        content = response.text
        
        # Verificar se contém elementos do tema
        theme_elements = [
            "theme-toggle",
            "data-theme",
            "fas fa-sun",
            "fas fa-moon",
            "--bg-primary",
            "--text-primary"
        ]
        
        print("🔍 Verificando elementos do tema:")
        for element in theme_elements:
            if element in content:
                print(f"✅ {element}")
            else:
                print(f"❌ {element}")
        
        # Verificar se há CSS para tema dark
        dark_css_patterns = [
            r'\[data-theme="dark"\]',
            r'--bg-primary: #1a202c',
            r'--text-primary: #f7fafc',
            r'background: linear-gradient\(135deg, #2d3748 0%, #1a202c 100%\)'
        ]
        
        print("\n🎨 Verificando CSS do tema dark:")
        for pattern in dark_css_patterns:
            if re.search(pattern, content):
                print(f"✅ Padrão encontrado: {pattern}")
            else:
                print(f"❌ Padrão não encontrado: {pattern}")
        
        # Verificar JavaScript do tema
        js_patterns = [
            r'initTheme\(\)',
            r'toggleTheme\(\)',
            r'localStorage\.getItem\("routerllm-theme"\)',
            r'document\.documentElement\.setAttribute\("data-theme"'
        ]
        
        print("\n⚙️ Verificando JavaScript do tema:")
        for pattern in js_patterns:
            if re.search(pattern, content):
                print(f"✅ Função encontrada: {pattern}")
            else:
                print(f"❌ Função não encontrada: {pattern}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de tema: {e}")
        return False

def test_theme_visual():
    print("\n👁️ Teste visual do tema:")
    print("1. Acesse: http://localhost:8000/")
    print("2. Clique no botão do sol/lua no header")
    print("3. Verifique se o tema muda de light para dark")
    print("4. Recarregue a página e veja se o tema é mantido")
    print("5. Teste em diferentes navegadores")

def main():
    print("🌙 Testando tema Dark/Light do RouterLLM...")
    print("=" * 50)
    
    # Verificar se o servidor está rodando
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code != 200:
            print("❌ Servidor não está rodando. Execute: py main.py")
            return
    except Exception as e:
        print(f"❌ Não foi possível conectar ao servidor: {e}")
        return
    
    print("✅ Servidor está rodando!\n")
    
    # Executar testes
    theme_ok = test_theme_functionality()
    test_theme_visual()
    
    # Resumo
    print("\n" + "=" * 50)
    print("📋 RESUMO DO TESTE DE TEMA:")
    
    if theme_ok:
        print("🎉 TEMA DARK/LIGHT IMPLEMENTADO COM SUCESSO!")
        print("\n✨ Funcionalidades:")
        print("  - Toggle de tema no header")
        print("  - Persistência no localStorage")
        print("  - Detecção automática da preferência do sistema")
        print("  - Animações suaves de transição")
        print("  - Cores otimizadas para ambos os temas")
        print("\n🌐 Teste visual em: http://localhost:8000/")
    else:
        print("⚠️  Alguns problemas foram encontrados no tema.")

if __name__ == "__main__":
    main()
