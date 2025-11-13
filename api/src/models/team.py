"""
Rugby Atlas - Team Model
Represents rugby teams (national teams, clubs, etc.)
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from ..core.db import Base


class Team(Base):
    """Team entity (national teams, clubs)"""
    
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    short_name = Column(String(100))
    code = Column(String(20))  # e.g., "ENG", "NZL"
    type = Column(String(50))  # "National", "Club", "Regional"
    country = Column(String(100))
    city = Column(String(100))
    logo_url = Column(String(500))
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    home_fixtures = relationship("Fixture", foreign_keys="Fixture.home_team_id", back_populates="home_team")
    away_fixtures = relationship("Fixture", foreign_keys="Fixture.away_team_id", back_populates="away_team")
    
    def __repr__(self):
        return f"<Team(id={self.id}, name='{self.name}', code='{self.code}')>"
