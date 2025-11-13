"""
Rugby Atlas - Competitions Router
API endpoints for competition management
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.db import get_db
from ..schemas.competition import CompetitionCreate, CompetitionUpdate, CompetitionResponse
from ..services.competition_service import CompetitionService

router = APIRouter(prefix="/competitions", tags=["competitions"])


@router.get("/", response_model=List[CompetitionResponse])
def get_competitions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all competitions with pagination"""
    competitions = CompetitionService.get_all(db, skip=skip, limit=limit)
    return competitions


@router.get("/{competition_id}", response_model=CompetitionResponse)
def get_competition(competition_id: int, db: Session = Depends(get_db)):
    """Get a specific competition by ID"""
    competition = CompetitionService.get_by_id(db, competition_id)
    if not competition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Competition with ID {competition_id} not found"
        )
    return competition


@router.post("/", response_model=CompetitionResponse, status_code=status.HTTP_201_CREATED)
def create_competition(competition_data: CompetitionCreate, db: Session = Depends(get_db)):
    """Create a new competition"""
    competition = CompetitionService.create(db, competition_data)
    return competition


@router.put("/{competition_id}", response_model=CompetitionResponse)
def update_competition(
    competition_id: int,
    competition_data: CompetitionUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing competition"""
    competition = CompetitionService.update(db, competition_id, competition_data)
    if not competition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Competition with ID {competition_id} not found"
        )
    return competition


@router.delete("/{competition_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_competition(competition_id: int, db: Session = Depends(get_db)):
    """Delete a competition (soft delete)"""
    success = CompetitionService.delete(db, competition_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Competition with ID {competition_id} not found"
        )
    return None
