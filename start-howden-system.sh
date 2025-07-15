#!/bin/bash

echo "🚀 Iniciando Sistema Howden - n8n + Agentic RAG"

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado. Por favor instala Docker Desktop."
    exit 1
fi

# Verificar docker-compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose no está instalado."
    exit 1
fi

# Crear directorios necesarios
mkdir -p n8n/custom-nodes
mkdir -p n8n/workflows

# Construir y levantar servicios
echo "🔧 Construyendo servicios..."
docker-compose build

echo "🚀 Iniciando servicios..."
docker-compose up -d

echo "⏳ Esperando a que los servicios estén listos..."
sleep 30

echo "✅ Sistema iniciado exitosamente!"
echo ""
echo "📊 Servicios disponibles:"
echo "- n8n: http://localhost:5678 (admin/admin123)"
echo "- Agentic RAG API: http://localhost:8058"
echo "- Neo4j Browser: http://localhost:7474 (neo4j/Jhonatanr1209)"
echo "- PostgreSQL: localhost:5432"
echo ""
echo "🎯 Próximos pasos:"
echo "1. Accede a n8n en http://localhost:5678"
echo "2. Importa el workflow desde n8n/workflows/howden-conciliation-workflow.json"
echo "3. Configura las credenciales de Agentic RAG API"
echo "4. Prueba el flujo con datos de ejemplo"
echo ""
echo "📚 Para más información, consulta el README.md"