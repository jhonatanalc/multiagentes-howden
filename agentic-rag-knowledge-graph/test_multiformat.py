#!/usr/bin/env python3
"""
Test script for multi-format document processing.
"""

import asyncio
import os
import logging
from pathlib import Path
import sys

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ingestion.document_processor import create_document_processor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


async def test_document_processing():
    """Test the document processor with various file types."""
    
    # Create document processor
    processor = create_document_processor()
    
    # Test files directory
    documents_dir = Path("Documents")
    
    if not documents_dir.exists():
        logger.error(f"Documents directory not found: {documents_dir}")
        return
    
    # Find all supported files
    supported_files = []
    for file_path in documents_dir.rglob("*"):
        if file_path.is_file() and processor.is_supported(str(file_path)):
            supported_files.append(file_path)
    
    if not supported_files:
        logger.warning("No supported files found in Documents directory")
        return
    
    logger.info(f"Found {len(supported_files)} supported files:")
    for file_path in supported_files:
        logger.info(f"  - {file_path}")
    
    # Process each file
    for file_path in supported_files:
        try:
            logger.info(f"\\nProcessing: {file_path}")
            
            result = await processor.process_document(str(file_path))
            
            # Print summary
            content = result['content']
            metadata = result['metadata']
            file_type = result['file_type']
            
            logger.info(f"File type: {file_type}")
            logger.info(f"Processor: {metadata.get('processor', 'unknown')}")
            logger.info(f"Content length: {len(content)} characters")
            
            # Print first few lines of content
            preview_lines = content.split('\\n')[:5]
            logger.info("Content preview:")
            for line in preview_lines:
                logger.info(f"  {line[:100]}...")
            
            if len(content.split('\\n')) > 5:
                logger.info(f"  ... and {len(content.split('\\n')) - 5} more lines")
            
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
    
    logger.info("\\nSupported file extensions:")
    for ext in processor.get_supported_extensions():
        logger.info(f"  {ext}")


if __name__ == "__main__":
    asyncio.run(test_document_processing())