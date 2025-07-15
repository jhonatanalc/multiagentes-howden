# Sistema Multi-Formato para Agentic RAG Knowledge Graph

## 🎯 Nuevas Capacidades

El sistema ahora puede procesar múltiples tipos de archivos:

### 📁 Formatos Soportados

- **📊 Excel**: `.xlsx`, `.xls`
- **📄 Word**: `.docx`, `.doc` (solo .docx completamente soportado)
- **📑 PDF**: `.pdf`
- **🖼️ Imágenes**: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`, `.gif` (con OCR)
- **📝 Texto**: `.md`, `.markdown`, `.txt`

### 🔧 Dependencias Agregadas

```bash
# Nuevas librerías en requirements.txt
pandas==2.2.2          # Para archivos Excel
openpyxl==3.1.2        # Para archivos Excel modernos
python-docx==1.1.2     # Para archivos Word
PyMuPDF==1.24.3        # Para archivos PDF
Pillow==10.3.0         # Para procesamiento de imágenes
pytesseract==0.3.10    # Para OCR en imágenes
markitdown==0.0.1a2    # Para procesamiento avanzado
```

### 🚀 Archivos Nuevos Creados

1. **`ingestion/document_processor.py`** - Procesador multi-formato principal
2. **`test_multiformat.py`** - Script de prueba para formatos
3. **`test_ingestion.py`** - Script de prueba para ingesta completa

### 🛠️ Archivos Modificados

1. **`requirements.txt`** - Nuevas dependencias
2. **`ingestion/ingest.py`** - Integración del procesador multi-formato
3. **`ingestion/__init__.py`** - Exportación del nuevo módulo
4. **`cli.py`** - Comando `files` para mostrar archivos soportados

## 🧪 Cómo Probar

### 1. Instalar Dependencias

```bash
# Activar entorno virtual
source venv/Scripts/activate  # Windows
# o
source venv/bin/activate      # Linux/Mac

# Instalar nuevas dependencias
pip install -r requirements.txt
```

### 2. Probar Procesamiento de Documentos

```bash
# Probar el procesador multi-formato
python test_multiformat.py

# Probar ingesta completa
python test_ingestion.py
```

### 3. Usar el CLI Actualizado

```bash
# Ejecutar CLI
python cli.py

# Dentro del CLI, usar nuevos comandos:
help     # Ver ayuda actualizada con tipos de archivo
files    # Ver archivos soportados y documentos actuales
```

### 4. Ingesta de Documentos

```bash
# Ingesta completa con todos los formatos
python -m ingestion.ingest --documents Documents --clean

# Ingesta rápida (sin knowledge graph)
python -m ingestion.ingest --documents Documents --fast
```

## 📊 Procesamiento por Tipo de Archivo

### Excel (.xlsx, .xls)
- **Procesador**: `pandas` + `openpyxl`
- **Salida**: Tablas convertidas a formato markdown
- **Características**: Procesa todas las hojas, mantiene estructura tabular

### Word (.docx)
- **Procesador**: `python-docx`
- **Salida**: Texto plano con tablas en markdown
- **Características**: Extrae párrafos y tablas

### PDF (.pdf)
- **Procesador**: `PyMuPDF`
- **Salida**: Texto por página
- **Características**: Extracción de texto página por página

### Imágenes (.jpg, .png, etc.)
- **Procesador**: `pytesseract` (OCR)
- **Salida**: Texto extraído de la imagen
- **Características**: Reconocimiento óptico de caracteres

### Texto (.md, .txt)
- **Procesador**: Lectura directa
- **Salida**: Contenido sin modificar
- **Características**: Soporte para múltiples codificaciones

## 🎯 Ejemplo de Uso

```python
from ingestion.document_processor import create_document_processor
import asyncio

async def procesar_documento():
    processor = create_document_processor()
    
    # Verificar si un archivo es soportado
    if processor.is_supported("Documents/GNP 17-23 JUN.xlsx"):
        # Procesar el documento
        result = await processor.process_document("Documents/GNP 17-23 JUN.xlsx")
        
        print(f"Tipo de archivo: {result['file_type']}")
        print(f"Procesador usado: {result['metadata']['processor']}")
        print(f"Contenido: {result['content'][:200]}...")

asyncio.run(procesar_documento())
```

## 🔍 Verificación de Archivos

Los archivos Excel que mencionaste están ahora soportados:
- `Documents/Del 04 julio al 10 Julio 2025.xlsx` ✅
- `Documents/Factura_INBURSA (2).xlsx` ✅
- `Documents/GNP 17-23 JUN (2).xlsx` ✅

## 🚨 Notas Importantes

1. **OCR**: Para imágenes se requiere `tesseract` instalado en el sistema
2. **Rendimiento**: Archivos grandes pueden tardar más en procesar
3. **Encoding**: El sistema maneja automáticamente diferentes codificaciones
4. **Fallback**: Si markitdown falla, usa procesadores específicos

## 📋 Próximos Pasos

1. Instalar las nuevas dependencias
2. Probar el procesamiento de tus archivos Excel
3. Ejecutar la ingesta completa
4. Verificar que los datos estén en Neo4j
5. Probar el workflow de n8n

¿Quieres que procedamos con la instalación y pruebas?