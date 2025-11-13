"""
Rugby Atlas - Governing Body Model
Represents governing bodies like World Rugby, Six Nations, etc.
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from ..core.db import Base


class GoverningBody(Base):
    """Governing body entity (e.g., World Rugby, Six Nations)"""
    
    __tablename__ = "governing_bodies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False)
    sport_id = Column(Integer, ForeignKey("sports.id"), nullable=False)
    website_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sport = relationship("Sport", back_populates="governing_bodies")
    competitions = relationship("Competition", back_populates="governing_body")
    
    def __repr__(self):
        return f"<GoverningBody(id={self.id}, name='{self.name}')>"
