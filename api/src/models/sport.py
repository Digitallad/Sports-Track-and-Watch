"""
Rugby Atlas - Sport Model
Represents different sports (Rugby Union, Rugby League, etc.)
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from ..core.db import Base


class Sport(Base):
    """Sport entity (e.g., Rugby Union, Rugby League)"""
    
    __tablename__ = "sports"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    code = Column(String(20), unique=True, nullable=False)  # e.g., "UNION", "LEAGUE"
    description = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    governing_bodies = relationship("GoverningBody", back_populates="sport")
    competitions = relationship("Competition", back_populates="sport")
    
    def __repr__(self):
        return f"<Sport(id={self.id}, name='{self.name}', code='{self.code}')>"
