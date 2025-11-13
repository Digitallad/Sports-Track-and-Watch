"""
Rugby Atlas - Fixture Model
Represents individual matches/fixtures
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from ..core.db import Base


class Fixture(Base):
    """Fixture entity (individual matches)"""
    
    __tablename__ = "fixtures"
    
    id = Column(Integer, primary_key=True, index=True)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)
    home_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    away_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    venue_id = Column(Integer, ForeignKey("venues.id"))
    
    # Match details
    match_date = Column(DateTime, nullable=False, index=True)
    round = Column(String(50))  # e.g., "Round 1", "Semi-Final"
    status = Column(String(50), default="scheduled")  # scheduled, live, completed, cancelled
    
    # Scores
    home_score = Column(Integer)
    away_score = Column(Integer)
    
    # External IDs for data sync
    external_id = Column(String(200), unique=True)
    source = Column(String(100))  # Data source identifier
    
    # Metadata
    notes = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    season = relationship("Season", back_populates="fixtures")
    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates="home_fixtures")
    away_team = relationship("Team", foreign_keys=[away_team_id], back_populates="away_fixtures")
    venue = relationship("Venue", back_populates="fixtures")
    rights = relationship("FixtureRights", back_populates="fixture")
    
    def __repr__(self):
        return f"<Fixture(id={self.id}, home_team_id={self.home_team_id}, away_team_id={self.away_team_id})>"
