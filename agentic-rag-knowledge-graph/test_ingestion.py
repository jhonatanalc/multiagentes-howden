#!/usr/bin/env python3
"""
Test script for multi-format document ingestion.
"""

import asyncio
import os
import logging
from pathlib import Path
import sys

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.models import IngestionConfig
from ingestion.ingest import DocumentIngestionPipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


async def test_ingestion():
    """Test the ingestion pipeline with multi-format documents."""
    
    # Create ingestion configuration
    config = IngestionConfig(
        chunk_size=1000,
        chunk_overlap=200,
        use_semantic_chunking=True,
        extract_entities=True,
        skip_graph_building=True  # Skip for faster testing
    )
    
    # Create pipeline
    pipeline = DocumentIngestionPipeline(
        config=config,
        documents_folder="Documents",
        clean_before_ingest=False  # Don't clean existing data
    )
    
    try:
        # Test finding files
        logger.info("Testing file discovery...")
        await pipeline.initialize()
        
        # Find supported files
        document_files = pipeline._find_document_files()
        logger.info(f"Found {len(document_files)} supported files:")
        for file_path in document_files:
            logger.info(f"  - {file_path}")
        
        if not document_files:
            logger.warning("No supported files found. Make sure you have documents in the Documents folder.")
            return
        
        # Test processing a single file
        if document_files:
            test_file = document_files[0]
            logger.info(f"\\nTesting single file processing: {test_file}")
            
            result = await pipeline._ingest_single_document(test_file)
            
            logger.info(f"Processing result:")
            logger.info(f"  Document ID: {result.document_id}")
            logger.info(f"  Title: {result.title}")
            logger.info(f"  Chunks created: {result.chunks_created}")
            logger.info(f"  Entities extracted: {result.entities_extracted}")
            logger.info(f"  Processing time: {result.processing_time_ms:.2f}ms")
            
            if result.errors:
                logger.warning(f"  Errors: {result.errors}")
            
        logger.info("\\nTesting complete!")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise
    finally:
        await pipeline.close()


if __name__ == "__main__":
    asyncio.run(test_ingestion())