"""
Rugby Atlas - Ingestion Models
DataSource and IngestionJob for tracking data ingestion
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON
from datetime import datetime

from ..core.db import Base


class DataSource(Base):
    """Data source entity (external APIs, feeds, etc.)"""
    
    __tablename__ = "data_sources"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, unique=True, index=True)
    code = Column(String(50), unique=True, nullable=False)
    type = Column(String(50))  # "API", "RSS", "Web Scraping", "Manual"
    
    # Connection details
    base_url = Column(String(500))
    auth_type = Column(String(50))  # "API_KEY", "OAuth", "None"
    credentials_ref = Column(String(200))  # Reference to secure credential storage
    
    # Configuration
    config = Column(JSON)  # JSON configuration
    
    # Status
    is_active = Column(Boolean, default=True)
    last_sync_at = Column(DateTime)
    next_sync_at = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<DataSource(id={self.id}, name='{self.name}', type='{self.type}')>"


class IngestionJob(Base):
    """Ingestion job tracking entity"""
    
    __tablename__ = "ingestion_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    data_source_id = Column(Integer, nullable=False)
    job_type = Column(String(50), nullable=False)  # "fixtures", "rights", "teams", etc.
    
    # Job details
    status = Column(String(50), default="pending")  # pending, running, completed, failed
    records_processed = Column(Integer, default=0)
    records_inserted = Column(Integer, default=0)
    records_updated = Column(Integer, default=0)
    records_failed = Column(Integer, default=0)
    
    # Timing
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    duration_seconds = Column(Integer)
    
    # Results
    error_message = Column(Text)
    result_summary = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<IngestionJob(id={self.id}, type='{self.job_type}', status='{self.status}')>"
