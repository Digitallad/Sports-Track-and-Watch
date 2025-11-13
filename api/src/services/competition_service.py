"""
Rugby Atlas - Competition Service
Business logic for competition management
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from ..models.competition import Competition
from ..schemas.competition import CompetitionCreate, CompetitionUpdate
from ..core.logging import get_logger

logger = get_logger(__name__)


class CompetitionService:
    """Service class for competition operations"""
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Competition]:
        """Get all competitions with pagination"""
        logger.info(f"Fetching competitions: skip={skip}, limit={limit}")
        return db.query(Competition).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, competition_id: int) -> Optional[Competition]:
        """Get a competition by ID"""
        logger.info(f"Fetching competition with ID: {competition_id}")
        return db.query(Competition).filter(Competition.id == competition_id).first()
    
    @staticmethod
    def get_by_code(db: Session, code: str) -> Optional[Competition]:
        """Get a competition by code"""
        logger.info(f"Fetching competition with code: {code}")
        return db.query(Competition).filter(Competition.code == code).first()
    
    @staticmethod
    def create(db: Session, competition_data: CompetitionCreate) -> Competition:
        """Create a new competition"""
        logger.info(f"Creating new competition: {competition_data.name}")
        competition = Competition(**competition_data.model_dump())
        db.add(competition)
        db.commit()
        db.refresh(competition)
        logger.info(f"Competition created successfully with ID: {competition.id}")
        return competition
    
    @staticmethod
    def update(db: Session, competition_id: int, competition_data: CompetitionUpdate) -> Optional[Competition]:
        """Update an existing competition"""
        logger.info(f"Updating competition with ID: {competition_id}")
        competition = db.query(Competition).filter(Competition.id == competition_id).first()
        if not competition:
            logger.warning(f"Competition with ID {competition_id} not found")
            return None
        
        update_data = competition_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(competition, key, value)
        
        db.commit()
        db.refresh(competition)
        logger.info(f"Competition {competition_id} updated successfully")
        return competition
    
    @staticmethod
    def delete(db: Session, competition_id: int) -> bool:
        """Delete a competition (soft delete)"""
        logger.info(f"Deleting competition with ID: {competition_id}")
        competition = db.query(Competition).filter(Competition.id == competition_id).first()
        if not competition:
            logger.warning(f"Competition with ID {competition_id} not found")
            return False
        
        competition.is_active = False
        db.commit()
        logger.info(f"Competition {competition_id} deleted successfully")
        return True
