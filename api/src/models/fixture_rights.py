"""
Rugby Atlas - Fixture Rights Model
Links fixtures to broadcast rights in specific territories
"""
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, String
from sqlalchemy.orm import relationship
from datetime import datetime

from ..core.db import Base


class FixtureRights(Base):
    """Fixture Rights entity (which provider has rights for a fixture in a territory)"""
    
    __tablename__ = "fixture_rights"
    
    id = Column(Integer, primary_key=True, index=True)
    fixture_id = Column(Integer, ForeignKey("fixtures.id"), nullable=False, index=True)
    territory_id = Column(Integer, ForeignKey("territories.id"), nullable=False, index=True)
    rights_package_id = Column(Integer, ForeignKey("rights_packages.id"))
    
    # Platform details
    platform_name = Column(String(200))
    platform_url = Column(String(500))
    
    # Availability
    is_live = Column(Boolean, default=True)
    is_on_demand = Column(Boolean, default=False)
    is_free = Column(Boolean, default=False)
    requires_subscription = Column(Boolean, default=True)
    
    # Metadata
    verified_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    fixture = relationship("Fixture", back_populates="rights")
    territory = relationship("Territory", back_populates="fixture_rights")
    
    def __repr__(self):
        return f"<FixtureRights(id={self.id}, fixture_id={self.fixture_id}, territory_id={self.territory_id})>"
