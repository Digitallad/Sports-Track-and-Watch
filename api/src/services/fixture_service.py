"""
Rugby Atlas - Fixture Service
Business logic for fixture management
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from ..models.fixture import Fixture
from ..schemas.fixture import FixtureCreate, FixtureUpdate
from ..core.logging import get_logger

logger = get_logger(__name__)


class FixtureService:
    """Service class for fixture operations"""
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Fixture]:
        """Get all fixtures with pagination"""
        logger.info(f"Fetching fixtures: skip={skip}, limit={limit}")
        return db.query(Fixture).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, fixture_id: int) -> Optional[Fixture]:
        """Get a fixture by ID"""
        logger.info(f"Fetching fixture with ID: {fixture_id}")
        return db.query(Fixture).filter(Fixture.id == fixture_id).first()
    
    @staticmethod
    def get_upcoming(db: Session, limit: int = 50) -> List[Fixture]:
        """Get upcoming fixtures"""
        logger.info(f"Fetching upcoming fixtures, limit={limit}")
        now = datetime.utcnow()
        return (
            db.query(Fixture)
            .filter(Fixture.match_date > now)
            .filter(Fixture.status == "scheduled")
            .order_by(Fixture.match_date)
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def get_by_team(db: Session, team_id: int, limit: int = 50) -> List[Fixture]:
        """Get fixtures for a specific team"""
        logger.info(f"Fetching fixtures for team ID: {team_id}")
        return (
            db.query(Fixture)
            .filter((Fixture.home_team_id == team_id) | (Fixture.away_team_id == team_id))
            .order_by(Fixture.match_date.desc())
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def create(db: Session, fixture_data: FixtureCreate) -> Fixture:
        """Create a new fixture"""
        logger.info(f"Creating new fixture: Team {fixture_data.home_team_id} vs {fixture_data.away_team_id}")
        fixture = Fixture(**fixture_data.model_dump())
        db.add(fixture)
        db.commit()
        db.refresh(fixture)
        logger.info(f"Fixture created successfully with ID: {fixture.id}")
        return fixture
    
    @staticmethod
    def update(db: Session, fixture_id: int, fixture_data: FixtureUpdate) -> Optional[Fixture]:
        """Update an existing fixture"""
        logger.info(f"Updating fixture with ID: {fixture_id}")
        fixture = db.query(Fixture).filter(Fixture.id == fixture_id).first()
        if not fixture:
            logger.warning(f"Fixture with ID {fixture_id} not found")
            return None
        
        update_data = fixture_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(fixture, key, value)
        
        db.commit()
        db.refresh(fixture)
        logger.info(f"Fixture {fixture_id} updated successfully")
        return fixture
    
    @staticmethod
    def delete(db: Session, fixture_id: int) -> bool:
        """Delete a fixture (soft delete)"""
        logger.info(f"Deleting fixture with ID: {fixture_id}")
        fixture = db.query(Fixture).filter(Fixture.id == fixture_id).first()
        if not fixture:
            logger.warning(f"Fixture with ID {fixture_id} not found")
            return False
        
        fixture.is_active = False
        db.commit()
        logger.info(f"Fixture {fixture_id} deleted successfully")
        return True
