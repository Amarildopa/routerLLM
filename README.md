# 🚀 RouterLLM - Seu Roteador Inteligente

Um roteador de modelos LLM que escolhe automaticamente o melhor modelo para cada tarefa, otimizando **custo** e **performance**.

## ✨ Features

- 🧠 **Roteamento Inteligente**: Analisa sua pergunta e escolhe o modelo ideal
- 💰 **Otimização de Custo**: Usa modelos baratos para tarefas simples, premium para complexas
- ⚡ **API REST**: Interface simples e rápida
- 📊 **Métricas**: Acompanhe uso, custo e performance
- 🔧 **Configurável**: Fácil de ajustar regras e adicionar novos modelos

## 🎯 Como Funciona

O RouterLLM analisa sua mensagem e decide qual modelo usar:

- **Perguntas simples** → `GPT-4o Mini` (rápido e barato)
- **Código/Debug** → `GPT-4` (precisão máxima)
- **Textos longos** → `Claude 3.5 Sonnet` (contexto gigante)
- **Conteúdo criativo** → `Gemini 1.5 Pro` (fluidez e criatividade)
- **Caso geral** → `Claude 3 Haiku` (balanceado)

## 🚀 Instalação

```bash
# Clone o projeto
git clone <seu-repo>
cd router_llm

# Instale dependências
pip install -r requirements.txt

# Execute
python main.py
```

## 📡 Uso da API

### Chat Básico
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Como fazer um loop em Python?"}'
```

### Forçar Modelo Específico
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Olá!", "force_model": "gpt-4o-mini"}'
```

### Ver Estatísticas
```bash
curl "http://localhost:8000/stats"
```

## ⚙️ Configuração

Edite `config.py` para:
- Adicionar novos modelos
- Ajustar custos
- Modificar regras de roteamento
- Configurar APIs dos provedores

## 🔧 Próximos Passos

1. **Integrar APIs reais** (OpenAI, Anthropic, Google)
2. **Adicionar autenticação**
3. **Implementar cache**
4. **Dashboard web**
5. **Métricas avançadas**

---

**Feito com ❤️ para otimizar seus custos com LLMs!**
