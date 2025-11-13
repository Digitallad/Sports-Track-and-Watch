"""
Rugby Atlas - Venue Model
Represents stadiums and venues
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from ..core.db import Base


class Venue(Base):
    """Venue entity (stadiums, arenas)"""
    
    __tablename__ = "venues"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    city = Column(String(100))
    country = Column(String(100))
    capacity = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    timezone = Column(String(100))  # IANA timezone
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    fixtures = relationship("Fixture", back_populates="venue")
    
    def __repr__(self):
        return f"<Venue(id={self.id}, name='{self.name}', city='{self.city}')>"
