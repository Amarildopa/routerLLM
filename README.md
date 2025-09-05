# 🚀 RouterLLM - Seu Roteador Inteligente

Um roteador de modelos LLM que escolhe automaticamente o melhor modelo para cada tarefa, otimizando **custo** e **performance**.

## ✨ Features

- 🧠 **Roteamento Inteligente**: Analisa sua pergunta e escolhe o modelo ideal
- 💰 **Otimização de Custo**: Usa modelos baratos para tarefas simples, premium para complexas
- ⚡ **API REST**: Interface simples e rápida
- 📊 **Dashboard Web**: Interface visual moderna com métricas em tempo real
- 📈 **Métricas Prometheus**: Monitoramento avançado e alertas
- 🔧 **Configurável**: Fácil de ajustar regras e adicionar novos modelos
- 🎯 **Teste Integrado**: Interface para testar a API diretamente no dashboard

## 🎯 Como Funciona

O RouterLLM analisa sua mensagem e decide qual modelo usar:

- **Perguntas simples** → `GPT-4o Mini` (rápido e barato)
- **Código/Debug** → `GPT-4` (precisão máxima)
- **Textos longos** → `Claude 3.5 Sonnet` (contexto gigante)
- **Conteúdo criativo** → `Gemini 1.5 Pro` (fluidez e criatividade)
- **Caso geral** → `Claude 3 Haiku` (balanceado)

## 🚀 Instalação

### Desenvolvimento Local
```bash
# Clone o projeto
git clone <seu-repo>
cd router_llm

# Instale dependências
pip install -r requirements.txt

# Configure as chaves de API
cp config.env.example .env
# Edite o arquivo .env com suas chaves

# Execute
python main.py
```

### Docker (Recomendado)
```bash
# Clone o projeto
git clone <seu-repo>
cd router_llm

# Configure as chaves de API
cp config.env.example .env
# Edite o arquivo .env com suas chaves

# Deploy automático
./deploy.sh dev

# Ou manualmente
docker-compose up -d
```

### Deploy em Produção
```bash
# Deploy em produção
./deploy.sh prod

# Ou usando docker-compose
docker-compose -f docker-compose.prod.yml up -d
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

### Home Page (Chat)
```bash
# Página inicial com chat integrado
http://localhost:8000/
```

### Dashboard Web
```bash
# Dashboard com métricas e configurações
http://localhost:8000/dashboard
```

### Configuração de APIs
```bash
# Tela para configurar chaves de API
http://localhost:8000/api-config
```

### Métricas Prometheus
```bash
curl "http://localhost:8000/metrics"
```

## ⚙️ Configuração

Edite `config.py` para:
- Adicionar novos modelos
- Ajustar custos
- Modificar regras de roteamento
- Configurar APIs dos provedores

## 🚀 Deploy em Produção

### Opções de Deploy

1. **Docker (Local/VPS)**
   ```bash
   ./deploy.sh prod
   ```

2. **Vercel (Serverless)**
   ```bash
   # Instale Vercel CLI
   npm i -g vercel
   
   # Configure as variáveis de ambiente
   vercel env add OPENAI_API_KEY
   vercel env add ANTHROPIC_API_KEY
   vercel env add GOOGLE_API_KEY
   
   # Deploy
   vercel --prod
   ```

3. **Railway/Render/Heroku**
   - Use o `Dockerfile` fornecido
   - Configure as variáveis de ambiente
   - Deploy automático

### Monitoramento
- Logs: `docker-compose logs -f`
- Health check: `curl http://localhost:8000/`
- Métricas: `curl http://localhost:8000/stats`

## 🔧 Próximos Passos

1. ✅ **APIs reais implementadas** (OpenAI, Anthropic, Google)
2. **Adicionar autenticação**
3. **Implementar cache Redis**
4. **Dashboard web**
5. **Métricas avançadas com Prometheus**

---

**Feito com ❤️ para otimizar seus custos com LLMs!**
