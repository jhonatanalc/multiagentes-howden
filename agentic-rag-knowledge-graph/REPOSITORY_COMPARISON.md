# Comparación de Sistemas de Chunking: Repositorio Base vs Actual

## Resumen Ejecutivo

**El problema**: El repositorio base generaba ~1500 chunks para archivos Excel grandes, mientras que el repositorio actual genera solo 1 chunk.

**Causa raíz**: Cambio fundamental en la arquitectura de chunking de un sistema genérico (repositorio base) a un sistema adaptativo especializado (repositorio actual) que maneja Excel de forma diferente.

---

## Análisis Detallado de Diferencias

### 1. **Arquitectura de Chunking**

#### **Repositorio Base** (`/Multiagents/agentic-rag-knowledge-graph/`)
```
✅ Sistema GENÉRICO
- SemanticChunker (único chunker inteligente)
- SimpleChunker (fallback básico)  
- TODOS los documentos procesados IGUAL
- Excel → Chunking semántico → Múltiples chunks pequeños
```

#### **Repositorio Actual** (`/agentic-rag-knowledge-graph/`)
```
❌ Sistema ADAPTATIVO (causó el problema)
- AdaptiveChunker (detecta tipo de archivo)
- Chunking específico por formato:
  - Excel → _chunk_excel() → Pocos chunks grandes
  - PDF → _chunk_pdf() 
  - Word → Chunking semántico
  - Imágenes → Chunks pequeños
```

---

### 2. **Configuración de IngestionConfig**

#### **Repositorio Base**
```python
class IngestionConfig(BaseModel):
    chunk_size: int = Field(default=1000, ge=100, le=5000)
    chunk_overlap: int = Field(default=200, ge=0, le=1000) 
    max_chunk_size: int = Field(default=2000, ge=500, le=10000)
    use_semantic_chunking: bool = True
    extract_entities: bool = True
    skip_graph_building: bool = Field(default=False)
    # NO HAY parámetros específicos por formato
```

#### **Repositorio Actual**
```python
class IngestionConfig(BaseModel):
    # Configuración base (igual)
    chunk_size: int = Field(default=1000, ge=100, le=5000)
    chunk_overlap: int = Field(default=200, ge=0, le=1000)
    max_chunk_size: int = Field(default=2000, ge=500, le=10000)
    use_semantic_chunking: bool = True
    extract_entities: bool = True
    skip_graph_building: bool = Field(default=False)
    
    # NUEVOS parámetros específicos por formato (causaron el problema)
    excel_rows_per_chunk: int = Field(default=50, ge=1, le=500)
    pdf_pages_per_chunk: int = Field(default=2, ge=1, le=10)
    image_ocr_chunk_size: int = Field(default=500, ge=100, le=2000)
```

---

### 3. **Script de Ingesta Excel Específico**

#### **Repositorio Base** (`ingest_excel_file.py`)
```python
# Configuración optimizada para Excel grandes
config = IngestionConfig(
    chunk_size=800,          # ← MÁS PEQUEÑO (más chunks)
    chunk_overlap=100,       # ← MENOR overlap
    use_semantic_chunking=True,  # ← HABILITADO = muchos chunks
    extract_entities=True,
    skip_graph_building=False
)
```

#### **Repositorio Actual** (usando endpoint)
```python
# Configuración por defecto desde API
config = IngestionConfig(
    chunk_size=1000,         # ← Valor por defecto
    excel_rows_per_chunk=50, # ← NUEVO: Agrupa por filas
    use_semantic_chunking=True
)
```

---

### 4. **Comportamiento de Chunking Excel**

#### **Repositorio Base - Flujo de Procesamiento**
```
Excel file → DocumentProcessor → Contenido texto plano
                ↓
SemanticChunker → _semantic_chunk() → Divide por estructura semántica
                ↓
chunk_size=800 + use_semantic_chunking=True
                ↓
RESULTADO: ~1500 chunks pequeños (promedio 800 caracteres)
```

#### **Repositorio Actual - Flujo de Procesamiento**
```
Excel file → DocumentProcessor → Contenido markdown table
                ↓
AdaptiveChunker.detect_document_type() → Detecta 'excel'
                ↓
_chunk_excel() → Agrupa por filas de tabla
                ↓
excel_rows_per_chunk=50 filas por chunk
                ↓
RESULTADO: Pocos chunks grandes (50 filas por chunk)
```

---

## ¿Por qué cambió el comportamiento?

### **En el Repositorio Base** (1500 chunks)
1. **Excel procesado como texto plano** → Contenido continuo sin estructura especial
2. **Chunking semántico genérico** → Divide por patrones de texto (párrafos, separadores)
3. **chunk_size=800** → Chunks más pequeños
4. **Sin agrupación por filas** → Cada sección de texto se chunka independientemente

### **En el Repositorio Actual** (1 chunk)
1. **Excel procesado como markdown table** → Estructura de tabla con `|` separadores
2. **AdaptiveChunker detecta tipo Excel** → Aplica `_chunk_excel()` especializado
3. **excel_rows_per_chunk=50** → Agrupa 50 filas en un solo chunk
4. **Si el Excel tiene <50 filas** → Solo 1 chunk
5. **Si markitdown falla** → Puede procesar todo como un bloque

---

## Soluciones Propuestas

### **Opción 1: Reducir `excel_rows_per_chunk`**
```python
config = IngestionConfig(
    excel_rows_per_chunk=5,  # En lugar de 50
    chunk_size=800           # Como en el repo base
)
```

### **Opción 2: Deshabilitar Excel especializado temporalmente**
```python
# Modificar AdaptiveChunker para usar chunking semántico en Excel
if file_type == 'excel':
    # return await self._chunk_excel(content, title, source, metadata)
    return await self.semantic_chunker.chunk_document(content, title, source, metadata)
```

### **Opción 3: Configuración híbrida**
```python
# Usar _chunk_excel() pero con fallback a semántico si genera pocos chunks
chunks = await self._chunk_excel(content, title, source, metadata)
if len(chunks) < 10:  # Si muy pocos chunks
    return await self.semantic_chunker.chunk_document(content, title, source, metadata)
return chunks
```

---

## Recomendación Final

**Para recuperar el comportamiento de 1500 chunks**:

1. **Ajustar configuración**: `excel_rows_per_chunk=5` (en lugar de 50)
2. **Reducir chunk_size**: De 1000 a 800 (como en el repo base)
3. **Implementar fallback**: Si Excel genera <50 chunks, usar chunking semántico

Esto mantendrá las ventajas del sistema adaptativo pero recuperará la granularidad del repositorio base para Excel grandes.