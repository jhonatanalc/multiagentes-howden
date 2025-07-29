#!/usr/bin/env python3
"""
Test script for the new adaptive chunker functionality.
"""

import asyncio
import os
import logging
from pathlib import Path
import sys

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ingestion.chunker import ChunkingConfig, AdaptiveChunker
from ingestion.document_processor import create_document_processor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


async def test_adaptive_chunker():
    """Test the adaptive chunker with various file types."""
    
    # Create chunker with Excel-optimized settings
    config = ChunkingConfig(
        chunk_size=1000,
        chunk_overlap=200,
        excel_rows_per_chunk=30,  # Smaller for testing
        pdf_pages_per_chunk=1,
        image_ocr_chunk_size=500,
        use_semantic_splitting=True
    )
    
    chunker = AdaptiveChunker(config)
    processor = create_document_processor()
    
    # Test files directory
    documents_dir = Path("Documents")
    
    if not documents_dir.exists():
        logger.error(f"Documents directory not found: {documents_dir}")
        return
    
    # Find test files
    test_files = []
    for file_path in documents_dir.rglob("*"):
        if file_path.is_file() and processor.is_supported(str(file_path)):
            test_files.append(file_path)
    
    if not test_files:
        logger.warning("No supported files found for testing")
        return
    
    logger.info(f"Testing adaptive chunker with {len(test_files)} files:")
    
    for file_path in test_files:
        try:
            logger.info(f"\n=== Processing: {file_path.name} ===")
            
            # Process document
            doc_result = await processor.process_document(str(file_path))
            content = doc_result['content']
            metadata = doc_result['metadata']
            
            logger.info(f"Document size: {len(content)} characters")
            logger.info(f"File type: {doc_result['file_type']}")
            logger.info(f"Processor: {metadata.get('processor', 'unknown')}")
            
            # Test chunking
            chunks = await chunker.chunk_document(
                content=content,
                title=file_path.stem,
                source=str(file_path),
                metadata=metadata
            )
            
            logger.info(f"Generated {len(chunks)} chunks")
            
            # Show chunk details
            for i, chunk in enumerate(chunks[:5]):  # Show first 5 chunks
                logger.info(f"  Chunk {i}: {len(chunk.content)} chars, method: {chunk.metadata.get('chunk_method', 'unknown')}")
                logger.info(f"    Preview: {chunk.content[:100]}...")
            
            if len(chunks) > 5:
                logger.info(f"  ... and {len(chunks) - 5} more chunks")
            
            # Summary
            total_chars = sum(len(chunk.content) for chunk in chunks)
            avg_chunk_size = total_chars / len(chunks) if chunks else 0
            logger.info(f"  Total content: {total_chars} chars, Average chunk size: {avg_chunk_size:.0f} chars")
            
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
    
    logger.info("\n=== Test completed ===")


if __name__ == "__main__":
    asyncio.run(test_adaptive_chunker())