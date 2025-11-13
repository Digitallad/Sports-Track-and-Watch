"""
Rugby Atlas - Ingestion Module
Data ingestion pipelines for fixtures, rights, and other data
"""
from .fixtures_ingestor import FixturesIngestor
from .rights_ingestor import RightsIngestor
from .sources_registry import SourcesRegistry

__all__ = [
    "FixturesIngestor",
    "RightsIngestor",
    "SourcesRegistry",
]
