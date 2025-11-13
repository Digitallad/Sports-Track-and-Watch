"""
Rugby Atlas - Rights Package Model
Represents broadcast rights packages
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Boolean, Text, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime

from ..core.db import Base


class RightsPackage(Base):
    """Rights package entity (broadcast rights agreements)"""
    
    __tablename__ = "rights_packages"
    
    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Coverage details
    competition_coverage = Column(Text)  # JSON or CSV of competition IDs
    territory_coverage = Column(Text)  # JSON or CSV of territory codes
    
    # Rights period
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    
    # Financial (optional)
    contract_value = Column(Numeric(15, 2))
    currency = Column(String(10))
    
    # Metadata
    is_exclusive = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    provider = relationship("Provider", back_populates="rights_packages")
    
    def __repr__(self):
        return f"<RightsPackage(id={self.id}, name='{self.name}', provider_id={self.provider_id})>"
