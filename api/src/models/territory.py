"""
Rugby Atlas - Territory Model
Represents geographic territories for broadcast rights
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from ..core.db import Base


class Territory(Base):
    """Territory entity for broadcast rights (countries/regions)"""
    
    __tablename__ = "territories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    code = Column(String(10), unique=True, nullable=False)  # ISO 3166-1 alpha-2/3
    region = Column(String(100))  # e.g., "Europe", "Asia Pacific"
    timezone = Column(String(100))  # IANA timezone
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    fixture_rights = relationship("FixtureRights", back_populates="territory")
    user_locations = relationship("UserLocation", back_populates="territory")
    
    def __repr__(self):
        return f"<Territory(id={self.id}, name='{self.name}', code='{self.code}')>"
