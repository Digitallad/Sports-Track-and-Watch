"""
Rugby Atlas - Sources Registry
Registry of external data sources and their configurations
"""
from typing import Dict, List, Optional
from enum import Enum

from ..core.logging import get_logger

logger = get_logger(__name__)


class SourceType(str, Enum):
    """Types of data sources"""
    API = "api"
    RSS = "rss"
    WEB_SCRAPING = "web_scraping"
    MANUAL = "manual"


class DataSourceConfig:
    """Configuration for a data source"""
    
    def __init__(
        self,
        id: int,
        name: str,
        code: str,
        source_type: SourceType,
        base_url: Optional[str] = None,
        auth_required: bool = False,
        config: Optional[Dict] = None
    ):
        self.id = id
        self.name = name
        self.code = code
        self.source_type = source_type
        self.base_url = base_url
        self.auth_required = auth_required
        self.config = config or {}


class SourcesRegistry:
    """
    Registry of all configured data sources.
    Provides centralized management of external data source configurations.
    """
    
    def __init__(self):
        self.sources: Dict[str, DataSourceConfig] = {}
        self.logger = logger
        self._initialize_sources()
    
    def _initialize_sources(self):
        """Initialize with predefined data sources"""
        # Placeholder sources - these would be configured from database or config files
        self.register_source(
            DataSourceConfig(
                id=1,
                name="World Rugby API",
                code="WORLD_RUGBY",
                source_type=SourceType.API,
                base_url="https://api.worldrugby.org",
                auth_required=True
            )
        )
        
        self.register_source(
            DataSourceConfig(
                id=2,
                name="Six Nations RSS",
                code="SIX_NATIONS",
                source_type=SourceType.RSS,
                base_url="https://www.sixnationsrugby.com/feed",
                auth_required=False
            )
        )
        
        self.logger.info(f"Initialized sources registry with {len(self.sources)} sources")
    
    def register_source(self, source: DataSourceConfig):
        """Register a new data source"""
        self.sources[source.code] = source
        self.logger.info(f"Registered data source: {source.name} ({source.code})")
    
    def get_source(self, code: str) -> Optional[DataSourceConfig]:
        """Get a data source by code"""
        return self.sources.get(code)
    
    def get_all_sources(self) -> List[DataSourceConfig]:
        """Get all registered data sources"""
        return list(self.sources.values())
    
    def get_sources_by_type(self, source_type: SourceType) -> List[DataSourceConfig]:
        """Get all sources of a specific type"""
        return [
            source for source in self.sources.values()
            if source.source_type == source_type
        ]
