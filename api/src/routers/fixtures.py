"""
Rugby Atlas - Fixtures Router
API endpoints for fixture management
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ..core.db import get_db
from ..schemas.fixture import FixtureCreate, FixtureUpdate, FixtureResponse
from ..services.fixture_service import FixtureService

router = APIRouter(prefix="/fixtures", tags=["fixtures"])


@router.get("/", response_model=List[FixtureResponse])
def get_fixtures(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all fixtures with pagination"""
    fixtures = FixtureService.get_all(db, skip=skip, limit=limit)
    return fixtures


@router.get("/upcoming", response_model=List[FixtureResponse])
def get_upcoming_fixtures(
    limit: int = Query(50, le=200),
    db: Session = Depends(get_db)
):
    """Get upcoming fixtures"""
    fixtures = FixtureService.get_upcoming(db, limit=limit)
    return fixtures


@router.get("/team/{team_id}", response_model=List[FixtureResponse])
def get_team_fixtures(
    team_id: int,
    limit: int = Query(50, le=200),
    db: Session = Depends(get_db)
):
    """Get fixtures for a specific team"""
    fixtures = FixtureService.get_by_team(db, team_id, limit=limit)
    return fixtures


@router.get("/{fixture_id}", response_model=FixtureResponse)
def get_fixture(fixture_id: int, db: Session = Depends(get_db)):
    """Get a specific fixture by ID"""
    fixture = FixtureService.get_by_id(db, fixture_id)
    if not fixture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fixture with ID {fixture_id} not found"
        )
    return fixture


@router.post("/", response_model=FixtureResponse, status_code=status.HTTP_201_CREATED)
def create_fixture(fixture_data: FixtureCreate, db: Session = Depends(get_db)):
    """Create a new fixture"""
    fixture = FixtureService.create(db, fixture_data)
    return fixture


@router.put("/{fixture_id}", response_model=FixtureResponse)
def update_fixture(
    fixture_id: int,
    fixture_data: FixtureUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing fixture"""
    fixture = FixtureService.update(db, fixture_id, fixture_data)
    if not fixture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fixture with ID {fixture_id} not found"
        )
    return fixture


@router.delete("/{fixture_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_fixture(fixture_id: int, db: Session = Depends(get_db)):
    """Delete a fixture (soft delete)"""
    success = FixtureService.delete(db, fixture_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fixture with ID {fixture_id} not found"
        )
    return None
