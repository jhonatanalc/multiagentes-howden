"""Ingestion package for processing documents into vector DB and knowledge graph."""

__version__ = "0.1.0"

from .document_processor import DocumentProcessor, create_document_processor

__all__ = ['DocumentProcessor', 'create_document_processor']