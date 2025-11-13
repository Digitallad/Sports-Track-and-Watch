"""
Rugby Atlas - Competition Model
Represents rugby competitions (Six Nations, Rugby Championship, etc.)
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from ..core.db import Base


class Competition(Base):
    """Competition entity (e.g., Six Nations, Rugby Championship)"""
    
    __tablename__ = "competitions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False)
    sport_id = Column(Integer, ForeignKey("sports.id"), nullable=False)
    governing_body_id = Column(Integer, ForeignKey("governing_bodies.id"))
    tier = Column(String(50))  # e.g., "International", "Domestic", "Club"
    format = Column(String(100))  # e.g., "League", "Knockout", "Hybrid"
    description = Column(Text)
    logo_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sport = relationship("Sport", back_populates="competitions")
    governing_body = relationship("GoverningBody", back_populates="competitions")
    seasons = relationship("Season", back_populates="competition")
    
    def __repr__(self):
        return f"<Competition(id={self.id}, name='{self.name}', code='{self.code}')>"
