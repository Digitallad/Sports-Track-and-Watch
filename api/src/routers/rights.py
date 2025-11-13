"""
Rugby Atlas - Rights Router
API endpoints for broadcast rights resolution
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.db import get_db
from ..services.rights_service import RightsService

router = APIRouter(prefix="/rights", tags=["rights"])


@router.get("/fixture/{fixture_id}/territory/{territory_id}")
def resolve_rights(
    fixture_id: int,
    territory_id: int,
    db: Session = Depends(get_db)
):
    """
    Resolve broadcast rights for a fixture in a specific territory.
    Returns information about where to watch the match.
    """
    rights = RightsService.resolve_rights(db, fixture_id, territory_id)
    if not rights:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No broadcast rights found for fixture {fixture_id} in territory {territory_id}"
        )
    return rights


@router.get("/fixture/{fixture_id}")
def get_fixture_rights(fixture_id: int, db: Session = Depends(get_db)):
    """Get all broadcast rights for a specific fixture"""
    rights = RightsService.get_by_fixture(db, fixture_id)
    return {"fixture_id": fixture_id, "rights": rights}
