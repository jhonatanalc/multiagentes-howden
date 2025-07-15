# Sistema Howden - Integración n8n + Agentic RAG

## Descripción General

Este sistema integra el flujo de conciliación de Howden (originalmente en graphs-orchestor) con un sistema de Agentic RAG usando n8n como orquestador visual y Neo4j como base de conocimiento.

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                      n8n Workflow                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Webhook   │  │  File       │  │  Agentic    │        │
│  │   Trigger   │→ │  Analysis   │→ │  RAG Node   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                Agentic RAG API                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Agent     │  │  Vector     │  │  Knowledge  │        │
│  │   Chat      │→ │  Search     │→ │  Graph      │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  Storage Layer                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ PostgreSQL  │  │    Neo4j    │  │  External   │        │
│  │ + pgvector  │  │   Graph     │  │  APIs       │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

## Componentes Principales

### 1. **n8n Workflow Engine**
- **Puerto**: 5678
- **Función**: Orquestación visual del flujo de conciliación
- **Características**:
  - Interfaz web para diseño de flujos
  - Nodos personalizados para Agentic RAG
  - Manejo de webhooks y triggers
  - Integración con APIs externas (SIGO, ACTUS)

### 2. **Agentic RAG Knowledge Graph**
- **Puerto**: 8058
- **Función**: Sistema de IA para procesamiento inteligente
- **Características**:
  - Búsqueda semántica con vectores
  - Grafo de conocimiento con Neo4j
  - Agentes conversacionales
  - Análisis de documentos

### 3. **Neo4j Graph Database**
- **Puerto**: 7474 (Browser), 7687 (Bolt)
- **Función**: Base de conocimiento estructurada
- **Características**:
  - Almacenamiento de entidades y relaciones
  - Consultas complejas con Cypher
  - Visualización de grafos
  - Persistencia de contexto

### 4. **PostgreSQL + pgvector**
- **Puerto**: 5432
- **Función**: Base de datos vectorial
- **Características**:
  - Almacenamiento de embeddings
  - Búsqueda por similitud
  - Metadatos de documentos
  - Historial de conversaciones

## Flujo de Procesamiento

### 1. **Entrada de Datos**
```
Webhook → Recibe archivos → Análisis inicial
```

### 2. **Extracción de Información**
```
Agentic RAG → Identifica entidades → Extrae fechas
```

### 3. **Búsqueda de Datos de Servicio**
```
Fechas identificadas → SIGO API → ACTUS API
```

### 4. **Conciliación Inteligente**
```
Datos de archivo + Datos de servicio → Agentic RAG → Resultados
```

### 5. **Generación de Informe**
```
Análisis IA → Explicaciones detalladas → Reporte final
```

## Instalación y Configuración

### Prerrequisitos
- Docker Desktop instalado
- Docker Compose disponible
- Puertos 5678, 8058, 7474, 7687, 5432 disponibles

### Pasos de Instalación

1. **Clonar repositorio y navegar al directorio**
   ```bash
   cd /path/to/howden/Multiagents
   ```

2. **Configurar variables de entorno**
   ```bash
   cp agentic-rag-knowledge-graph/.env.example agentic-rag-knowledge-graph/.env
   # Editar .env con las credenciales apropiadas
   ```

3. **Iniciar sistema**
   ```bash
   chmod +x start-howden-system.sh
   ./start-howden-system.sh
   ```

4. **Acceder a n8n**
   - URL: http://localhost:5678
   - Usuario: admin
   - Contraseña: admin123

5. **Importar workflow**
   - Ir a n8n interface
   - Importar `n8n/workflows/howden-conciliation-workflow.json`

## Configuración de Credenciales

### En n8n:
1. Ir a "Credentials" → "Create New"
2. Seleccionar "Agentic RAG API"
3. Configurar:
   - Base URL: `http://agentic-rag:8058`
   - API Key: (opcional)

### Variables de Entorno:
```bash
# Agentic RAG
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/howden_rag
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=Jhonatanr1209
OPENAI_API_KEY=sk-proj-...

# SIGO API
SIGO_API_BASE_URL=https://enginia.grupordas.com.mx/...
SIGO_API_USER=RocketCode
SIGO_API_PASSWORD=R0ck3tC083
SIGO_API_TOKEN=TWV4aWNhbm9z...

# ACTUS API
ACTUS_API_BASE_URL=https://hmexportalapi.howdengroup.com/...
ACTUS_API_USER=UsrConsRocketCode
ACTUS_API_PASSWORD=HwdConR#15!
```

## Uso del Sistema

### 1. **Activar Workflow**
- En n8n, activar el workflow "Howden Conciliation"
- El webhook estará disponible en: `http://localhost:5678/webhook/conciliation`

### 2. **Enviar Datos**
```bash
curl -X POST http://localhost:5678/webhook/conciliation \
  -H "Content-Type: application/json" \
  -d '{
    "files": ["path/to/file1.xlsx", "path/to/file2.pdf"],
    "sessionId": "session_123"
  }'
```

### 3. **Visualizar Resultados**
- En n8n: Ver ejecuciones y logs
- En Neo4j Browser: Explorar grafo de conocimiento
- En respuesta: Recibir informe detallado

## Personalización

### Agregar Nuevos Nodos
1. Crear nodo en `n8n/custom-nodes/`
2. Implementar lógica específica
3. Integrar con Agentic RAG API

### Modificar Flujo
1. Abrir workflow en n8n
2. Agregar/modificar nodos
3. Configurar conexiones
4. Probar y activar

### Extender Conocimiento
1. Agregar documentos a `agentic-rag-knowledge-graph/documents/`
2. Ejecutar ingestion: `python -m ingestion.ingest`
3. Verificar en Neo4j Browser

## Monitoreo y Debugging

### Logs de Servicios
```bash
docker-compose logs -f agentic-rag
docker-compose logs -f n8n
docker-compose logs -f neo4j
```

### Verificar Estado
```bash
# Verificar servicios
docker-compose ps

# Verificar APIs
curl http://localhost:8058/health
curl http://localhost:5678/healthz
```

### Neo4j Browser
- URL: http://localhost:7474
- Usuario: neo4j
- Contraseña: Jhonatanr1209

## Comparación con graphs-orchestor

| Aspecto | graphs-orchestor | n8n + Agentic RAG |
|---------|------------------|-------------------|
| Orquestación | LangGraph (código) | n8n (visual) |
| Conocimiento | En memoria | Neo4j persistente |
| Escalabilidad | Limitada | Contenedores |
| Visualización | Mermaid estático | n8n dinámico |
| Mantenimiento | Código complejo | Interfaz visual |
| Explicabilidad | Logs técnicos | IA conversacional |

## Ventajas del Nuevo Sistema

1. **Visualización**: Flujos visibles y editables
2. **Escalabilidad**: Arquitectura en contenedores
3. **Conocimiento**: Grafo persistente y consultable
4. **Explicabilidad**: IA que explica sus decisiones
5. **Mantenimiento**: Interfaz visual vs código
6. **Integración**: APIs estándar y webhooks
7. **Monitoreo**: Logs centralizados y métricas

## Próximos Pasos

1. **Pruebas**: Validar con datos reales de Howden
2. **Optimización**: Ajustar parámetros de IA
3. **Documentación**: Crear guías de usuario
4. **Integración**: Conectar con sistemas existentes
5. **Escalamiento**: Configurar para producción

## Soporte

Para soporte técnico:
- Revisar logs en Docker Compose
- Consultar Neo4j Browser para datos
- Verificar configuración de credenciales
- Revisar documentación de APIs