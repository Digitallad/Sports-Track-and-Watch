"""
Rugby Atlas - Provider Model
Represents broadcast providers (Sky Sports, ESPN, etc.)
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from ..core.db import Base


class Provider(Base):
    """Provider entity (broadcast/streaming companies)"""
    
    __tablename__ = "providers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False)
    type = Column(String(50))  # "TV", "Streaming", "Hybrid"
    website_url = Column(String(500))
    logo_url = Column(String(500))
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    platforms = relationship("Platform", back_populates="provider")
    rights_packages = relationship("RightsPackage", back_populates="provider")
    
    def __repr__(self):
        return f"<Provider(id={self.id}, name='{self.name}', code='{self.code}')>"
