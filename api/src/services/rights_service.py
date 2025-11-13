"""
Rugby Atlas - Rights Service
Business logic for broadcast rights management
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from ..models.fixture_rights import FixtureRights
from ..core.logging import get_logger

logger = get_logger(__name__)


class RightsService:
    """Service class for broadcast rights operations"""
    
    @staticmethod
    def get_by_fixture(db: Session, fixture_id: int) -> List[FixtureRights]:
        """Get all rights for a specific fixture"""
        logger.info(f"Fetching rights for fixture ID: {fixture_id}")
        return db.query(FixtureRights).filter(FixtureRights.fixture_id == fixture_id).all()
    
    @staticmethod
    def get_by_fixture_and_territory(
        db: Session, fixture_id: int, territory_id: int
    ) -> Optional[FixtureRights]:
        """Get rights for a fixture in a specific territory"""
        logger.info(f"Fetching rights for fixture {fixture_id} in territory {territory_id}")
        return (
            db.query(FixtureRights)
            .filter(
                FixtureRights.fixture_id == fixture_id,
                FixtureRights.territory_id == territory_id,
                FixtureRights.is_active == True
            )
            .first()
        )
    
    @staticmethod
    def resolve_rights(db: Session, fixture_id: int, territory_id: int) -> Optional[dict]:
        """
        Resolve broadcast rights for a fixture in a territory.
        This is a placeholder implementation that will be enhanced by the rights engine.
        """
        logger.info(f"Resolving rights for fixture {fixture_id} in territory {territory_id}")
        rights = RightsService.get_by_fixture_and_territory(db, fixture_id, territory_id)
        
        if not rights:
            logger.warning(f"No rights found for fixture {fixture_id} in territory {territory_id}")
            return None
        
        return {
            "fixture_id": fixture_id,
            "territory_id": territory_id,
            "platform_name": rights.platform_name,
            "platform_url": rights.platform_url,
            "is_live": rights.is_live,
            "is_on_demand": rights.is_on_demand,
            "is_free": rights.is_free,
            "requires_subscription": rights.requires_subscription,
        }
    
    @staticmethod
    def create(db: Session, fixture_id: int, territory_id: int, **kwargs) -> FixtureRights:
        """Create a new fixture rights entry"""
        logger.info(f"Creating rights entry for fixture {fixture_id} in territory {territory_id}")
        rights = FixtureRights(
            fixture_id=fixture_id,
            territory_id=territory_id,
            **kwargs
        )
        db.add(rights)
        db.commit()
        db.refresh(rights)
        logger.info(f"Rights entry created successfully with ID: {rights.id}")
        return rights
    
    @staticmethod
    def delete(db: Session, rights_id: int) -> bool:
        """Delete a rights entry (soft delete)"""
        logger.info(f"Deleting rights entry with ID: {rights_id}")
        rights = db.query(FixtureRights).filter(FixtureRights.id == rights_id).first()
        if not rights:
            logger.warning(f"Rights entry with ID {rights_id} not found")
            return False
        
        rights.is_active = False
        db.commit()
        logger.info(f"Rights entry {rights_id} deleted successfully")
        return True
