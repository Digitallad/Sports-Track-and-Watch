"""
Rugby Atlas - Season Model
Represents competition seasons
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from ..core.db import Base


class Season(Base):
    """Season entity for competitions"""
    
    __tablename__ = "seasons"
    
    id = Column(Integer, primary_key=True, index=True)
    competition_id = Column(Integer, ForeignKey("competitions.id"), nullable=False)
    name = Column(String(100), nullable=False)  # e.g., "2024"
    year = Column(Integer, nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    is_current = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    competition = relationship("Competition", back_populates="seasons")
    fixtures = relationship("Fixture", back_populates="season")
    
    def __repr__(self):
        return f"<Season(id={self.id}, competition_id={self.competition_id}, name='{self.name}')>"
