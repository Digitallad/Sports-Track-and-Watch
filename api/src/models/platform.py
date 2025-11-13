"""
Rugby Atlas - Platform Model
Represents specific platforms/channels within providers
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from ..core.db import Base


class Platform(Base):
    """Platform entity (specific channels/apps within providers)"""
    
    __tablename__ = "platforms"
    
    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=False)
    name = Column(String(200), nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    type = Column(String(50))  # "Linear TV", "App", "Website"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    provider = relationship("Provider", back_populates="platforms")
    
    def __repr__(self):
        return f"<Platform(id={self.id}, name='{self.name}', provider_id={self.provider_id})>"
