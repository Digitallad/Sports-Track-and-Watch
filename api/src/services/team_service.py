"""
Rugby Atlas - Team Service
Business logic for team management
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from ..models.team import Team
from ..schemas.team import TeamCreate, TeamUpdate
from ..core.logging import get_logger

logger = get_logger(__name__)


class TeamService:
    """Service class for team operations"""
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Team]:
        """Get all teams with pagination"""
        logger.info(f"Fetching teams: skip={skip}, limit={limit}")
        return db.query(Team).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, team_id: int) -> Optional[Team]:
        """Get a team by ID"""
        logger.info(f"Fetching team with ID: {team_id}")
        return db.query(Team).filter(Team.id == team_id).first()
    
    @staticmethod
    def get_by_code(db: Session, code: str) -> Optional[Team]:
        """Get a team by code"""
        logger.info(f"Fetching team with code: {code}")
        return db.query(Team).filter(Team.code == code).first()
    
    @staticmethod
    def create(db: Session, team_data: TeamCreate) -> Team:
        """Create a new team"""
        logger.info(f"Creating new team: {team_data.name}")
        team = Team(**team_data.model_dump())
        db.add(team)
        db.commit()
        db.refresh(team)
        logger.info(f"Team created successfully with ID: {team.id}")
        return team
    
    @staticmethod
    def update(db: Session, team_id: int, team_data: TeamUpdate) -> Optional[Team]:
        """Update an existing team"""
        logger.info(f"Updating team with ID: {team_id}")
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team:
            logger.warning(f"Team with ID {team_id} not found")
            return None
        
        update_data = team_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(team, key, value)
        
        db.commit()
        db.refresh(team)
        logger.info(f"Team {team_id} updated successfully")
        return team
    
    @staticmethod
    def delete(db: Session, team_id: int) -> bool:
        """Delete a team (soft delete by setting is_active=False)"""
        logger.info(f"Deleting team with ID: {team_id}")
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team:
            logger.warning(f"Team with ID {team_id} not found")
            return False
        
        team.is_active = False
        db.commit()
        logger.info(f"Team {team_id} deleted successfully")
        return True
