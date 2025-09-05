#!/bin/bash

# 🚀 Script de Deploy do RouterLLM
# Uso: ./deploy.sh [dev|prod]

set -e

ENVIRONMENT=${1:-dev}

echo "🚀 Iniciando deploy do RouterLLM em modo: $ENVIRONMENT"

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando. Inicie o Docker e tente novamente."
    exit 1
fi

# Verificar se arquivo .env existe
if [ ! -f .env ]; then
    echo "⚠️  Arquivo .env não encontrado. Copiando .env.example..."
    cp .env.example .env
    echo "📝 Configure suas chaves de API no arquivo .env antes de continuar."
    exit 1
fi

# Build da imagem
echo "🔨 Construindo imagem Docker..."
docker build -t router-llm:latest .

if [ "$ENVIRONMENT" = "prod" ]; then
    echo "🚀 Deploy em produção..."
    docker-compose -f docker-compose.prod.yml up -d
    echo "✅ RouterLLM está rodando em produção!"
    echo "🌐 Acesse: http://localhost:8000"
    echo "📊 Documentação: http://localhost:8000/docs"
else
    echo "🚀 Deploy em desenvolvimento..."
    docker-compose up -d
    echo "✅ RouterLLM está rodando em desenvolvimento!"
    echo "🌐 Acesse: http://localhost:8000"
    echo "📊 Documentação: http://localhost:8000/docs"
fi

echo ""
echo "📋 Comandos úteis:"
echo "  - Ver logs: docker-compose logs -f"
echo "  - Parar: docker-compose down"
echo "  - Status: docker-compose ps"

