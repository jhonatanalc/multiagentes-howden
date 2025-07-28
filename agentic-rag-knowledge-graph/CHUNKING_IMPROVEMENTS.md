# Mejoras en el Sistema de Chunking

## Problema Identificado

El sistema anterior solo generaba 1 chunk para archivos Excel grandes (5000+ filas) debido a:

1. **Chunking semántico mal configurado**: Los patrones de splitting estaban diseñados para Markdown, no para tablas Excel
2. **Configuración por defecto inadecuada**: `chunk_size=1000` y `max_chunk_size=2000` muy pequeños para documentos grandes
3. **Falta de estrategias específicas por tipo de documento**

## Solución Implementada: AdaptiveChunker

### 1. **Chunker Inteligente por Tipo de Documento**

Se creó `AdaptiveChunker` que detecta automáticamente el tipo de documento y aplica la estrategia óptima:

```python
# Detección automática de tipo
file_type = self._detect_document_type(source, metadata)

# Estrategias específicas
if file_type == 'excel':
    return await self._chunk_excel(content, title, source, metadata)
elif file_type == 'pdf':
    return await self._chunk_pdf(content, title, source, metadata)
elif file_type == 'word':
    return await self._chunk_word(content, title, source, metadata)
elif file_type == 'image':
    return await self._chunk_image(content, title, source, metadata)
```

### 2. **Chunking Específico para Excel**

**Problema anterior**: Excel con 5000 filas → 1 chunk gigante
**Solución nueva**: Excel dividido por número configurable de filas

```python
async def _chunk_excel(self, content: str, title: str, source: str, metadata):
    """Chunk Excel content by table rows."""
    
    # Split content by table rows (Excel converted to markdown tables)
    chunks = []
    current_chunk = ""
    current_row_count = 0
    
    for line in lines:
        # Check if this is a table row (starts with |)
        if line.strip().startswith('|') and '|' in line.strip()[1:]:
            if current_row_count >= self.config.excel_rows_per_chunk:
                # Save current chunk and start new one
                chunks.append(current_chunk.strip())
                current_chunk = line
                current_row_count = 1
            else:
                current_chunk += '\n' + line
                current_row_count += 1
```

**Resultado**: Excel con 5000 filas + `excel_rows_per_chunk=50` → **100 chunks**

### 3. **Configuración Mejorada**

Se añadieron parámetros específicos por formato:

```python
class IngestionConfig(BaseModel):
    # Configuración original
    chunk_size: int = 1000
    chunk_overlap: int = 200
    max_chunk_size: int = 2000
    
    # Nuevos parámetros específicos por formato
    excel_rows_per_chunk: int = 50        # Filas Excel por chunk
    pdf_pages_per_chunk: int = 2          # Páginas PDF por chunk  
    image_ocr_chunk_size: int = 500       # Tamaño chunk para OCR
```

### 4. **Endpoint API Mejorado**

El endpoint `/documents/process-existing` ahora acepta parámetros configurables:

```python
@app.post("/documents/process-existing")
async def process_existing_documents(
    excel_rows_per_chunk: int = 50,      # Configurable por request
    pdf_pages_per_chunk: int = 2,
    chunk_size: int = 1000,
    clean_existing: bool = False
):
```

## Estrategias por Tipo de Documento

### 📊 **Excel (.xlsx, .xls)**
- **Método**: División por filas de tabla
- **Configuración**: `excel_rows_per_chunk=50` (por defecto)
- **Ventaja**: Mantiene estructura tabular, chunks de tamaño predecible

### 📄 **PDF (.pdf)** 
- **Método**: División por páginas
- **Configuración**: `pdf_pages_per_chunk=2` (por defecto)
- **Fallback**: Si no hay marcadores de página, usa chunking semántico

### 📝 **Word (.docx, .doc)**
- **Método**: Chunking semántico (mantiene estructura de párrafos)
- **Ventaja**: Respeta formato de documento estructurado

### 🖼️ **Imágenes (.jpg, .png, etc.)**
- **Método**: Chunking simple con tamaño reducido
- **Configuración**: `image_ocr_chunk_size=500` (OCR text suele ser fragmentado)

### 📋 **Markdown/Texto (.md, .txt)**
- **Método**: Chunking semántico (comportamiento original)
- **Ventaja**: Respeta estructura markdown (headers, listas, etc.)

## Uso y Configuración

### 1. **Uso básico (valores por defecto)**
```bash
POST /documents/process-existing
```

### 2. **Configuración personalizada para Excel grandes**
```bash
POST /documents/process-existing?excel_rows_per_chunk=100&chunk_size=1500
```

### 3. **Procesamiento rápido con chunks grandes**
```bash  
POST /documents/process-existing?excel_rows_per_chunk=200&pdf_pages_per_chunk=5&clean_existing=true
```

## Resultados Esperados

### **Antes**:
- Excel 5000 filas → **1 chunk** (problema)
- PDF 10 páginas → **1-2 chunks** 
- Word 50 páginas → **Chunks inconsistentes**

### **Después**:
- Excel 5000 filas → **100 chunks** (50 filas c/u)
- PDF 10 páginas → **5 chunks** (2 páginas c/u)
- Word 50 páginas → **Chunks semánticos** (párrafos/secciones)
- Imágenes OCR → **Chunks pequeños** (500 chars c/u)

## Testing

Para probar las mejoras:

```bash
# Test local del chunker adaptativo
python3 test_adaptive_chunker.py

# Test del endpoint mejorado
curl -X POST "http://localhost:8000/documents/process-existing?excel_rows_per_chunk=30"
```

## Beneficios

1. ✅ **Soluciona el problema principal**: Excel grandes ahora generan múltiples chunks
2. ✅ **Configuración flexible**: Parámetros ajustables por request
3. ✅ **Soporte multi-formato**: Excel, PDF, Word, imágenes, Markdown
4. ✅ **Backward compatible**: Funciona con documentos existentes
5. ✅ **Metadata enriquecida**: Cada chunk incluye método de chunking usado
6. ✅ **Fallbacks inteligentes**: Si una estrategia falla, usa alternativa