"""
Rugby Atlas - Rights Resolution Engine
Core engine for resolving broadcast rights based on fixtures, territories, and rules
"""
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from ..core.logging import get_logger
from ..models.fixture_rights import FixtureRights
from ..models.fixture import Fixture
from ..models.territory import Territory
from .rules import RuleEvaluator

logger = get_logger(__name__)


class RightsResolutionEngine:
    """
    Engine for resolving broadcast rights.
    Determines which providers have rights to broadcast a fixture in a specific territory.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.logger = logger
        self.rule_evaluator = RuleEvaluator()
    
    def resolve_for_fixture(
        self,
        fixture_id: int,
        territory_id: int,
        user_context: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Resolve broadcast rights for a fixture in a specific territory.
        
        Args:
            fixture_id: ID of the fixture
            territory_id: ID of the territory
            user_context: Optional user context for personalization
        
        Returns:
            Dictionary with resolved rights information or None if no rights found
        """
        self.logger.info(f"Resolving rights for fixture {fixture_id} in territory {territory_id}")
        
        # Fetch fixture
        fixture = self.db.query(Fixture).filter(Fixture.id == fixture_id).first()
        if not fixture:
            self.logger.warning(f"Fixture {fixture_id} not found")
            return None
        
        # Fetch territory
        territory = self.db.query(Territory).filter(Territory.id == territory_id).first()
        if not territory:
            self.logger.warning(f"Territory {territory_id} not found")
            return None
        
        # Find applicable rights
        rights = self._find_applicable_rights(fixture_id, territory_id)
        
        if not rights:
            self.logger.info(f"No rights found for fixture {fixture_id} in territory {territory_id}")
            return None
        
        # Apply business rules
        resolved_rights = self._apply_resolution_rules(rights, fixture, territory, user_context)
        
        return resolved_rights
    
    def _find_applicable_rights(
        self,
        fixture_id: int,
        territory_id: int
    ) -> List[FixtureRights]:
        """
        Find all applicable rights for a fixture in a territory.
        """
        rights = (
            self.db.query(FixtureRights)
            .filter(
                FixtureRights.fixture_id == fixture_id,
                FixtureRights.territory_id == territory_id,
                FixtureRights.is_active == True
            )
            .all()
        )
        
        self.logger.info(f"Found {len(rights)} rights entries")
        return rights
    
    def _apply_resolution_rules(
        self,
        rights: List[FixtureRights],
        fixture: Fixture,
        territory: Territory,
        user_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Apply business rules to resolve the best rights option.
        This is a placeholder for complex resolution logic.
        """
        # For now, return the first rights entry
        # In production, this would evaluate rules based on:
        # - Exclusivity
        # - User subscription status
        # - Geographic restrictions
        # - Blackout rules
        # - Time-based availability
        
        primary_rights = rights[0] if rights else None
        
        if not primary_rights:
            return None
        
        return {
            "fixture_id": fixture.id,
            "territory_id": territory.id,
            "territory_name": territory.name,
            "platform_name": primary_rights.platform_name,
            "platform_url": primary_rights.platform_url,
            "is_live": primary_rights.is_live,
            "is_on_demand": primary_rights.is_on_demand,
            "is_free": primary_rights.is_free,
            "requires_subscription": primary_rights.requires_subscription,
            "alternative_options": len(rights) - 1 if len(rights) > 1 else 0
        }
    
    def resolve_bulk(
        self,
        fixture_ids: List[int],
        territory_id: int
    ) -> Dict[int, Optional[Dict[str, Any]]]:
        """
        Bulk resolve rights for multiple fixtures in a territory.
        Useful for resolving rights for an entire competition schedule.
        """
        self.logger.info(f"Bulk resolving rights for {len(fixture_ids)} fixtures in territory {territory_id}")
        
        results = {}
        for fixture_id in fixture_ids:
            results[fixture_id] = self.resolve_for_fixture(fixture_id, territory_id)
        
        return results
