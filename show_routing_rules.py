#!/usr/bin/env python3
"""
🧠 Mostrar regras de roteamento do RouterLLM
"""

from config import RouterConfig
from router import LLMRouter

def show_routing_rules():
    print("🧠 REGRAS DE ROTEAMENTO DO ROUTERLLM")
    print("=" * 50)
    
    # Inicializar configuração
    config = RouterConfig()
    router = LLMRouter(config)
    
    # Mostrar modelos disponíveis
    available_models = config.get_available_models()
    print(f"\n📊 MODELOS DISPONÍVEIS: {len(available_models)}")
    for model, info in available_models.items():
        print(f"  ✅ {model}: {info['use_case']}")
    
    print(f"\n❌ MODELOS INDISPONÍVEIS: {len(config.models) - len(available_models)}")
    for model, info in config.models.items():
        if model not in available_models:
            print(f"  ❌ {model}: {info['use_case']} (Chave de API necessária)")
    
    # Mostrar regras
    print(f"\n🎯 REGRAS DE ROTEAMENTO:")
    print("=" * 50)
    
    print("\n1. 🔧 CÓDIGO/PROGRAMAÇÃO")
    print("   Palavras-chave: código, code, python, javascript, sql, debug, erro, função, class, import")
    print("   Prioridade: gpt-4 → claude-3-5-sonnet → gpt-4o-mini")
    print("   Motivo: Precisão máxima para programação")
    
    print("\n2. ⚡ PERGUNTAS SIMPLES (< 100 caracteres)")
    print("   Padrões: 'o que é', 'como', 'quando', 'onde', 'quem', 'sim ou não'")
    print("   Prioridade: gpt-4o-mini → claude-3-haiku → gpt-4")
    print("   Motivo: Rápido e econômico para perguntas simples")
    
    print("\n3. 📄 TEXTOS LONGOS (> 1000 caracteres)")
    print("   Prioridade: claude-3-5-sonnet → gemini-1.5-pro → gpt-4")
    print("   Motivo: Contexto extenso para análises profundas")
    
    print("\n4. 🎨 CONTEÚDO CRIATIVO")
    print("   Palavras-chave: criativo, marketing, copy, slogan, história, poema, roteiro")
    print("   Prioridade: gemini-1.5-pro → claude-3-5-sonnet → gpt-4")
    print("   Motivo: Fluidez e criatividade")
    
    print("\n5. ⚖️ CASO GERAL")
    print("   Prioridade: claude-3-haiku → gpt-4o-mini → gpt-4")
    print("   Motivo: Balanceado entre qualidade e custo")
    
    # Testar exemplos
    print(f"\n🧪 EXEMPLOS DE ROTEAMENTO:")
    print("=" * 50)
    
    test_messages = [
        "Como fazer um loop em Python?",
        "O que é inteligência artificial?",
        "Escreva um poema sobre tecnologia",
        "Analise este texto longo sobre economia global e suas implicações...",
        "Olá, como você está?"
    ]
    
    for message in test_messages:
        try:
            model, reasoning = router.route_request(message)
            print(f"\n💬 '{message[:30]}...'")
            print(f"   → Modelo: {model}")
            print(f"   → Raciocínio: {reasoning}")
        except Exception as e:
            print(f"\n💬 '{message[:30]}...'")
            print(f"   → Erro: {e}")

if __name__ == "__main__":
    show_routing_rules()
