"""
Rugby Atlas - Teams Router
API endpoints for team management
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.db import get_db
from ..schemas.team import TeamCreate, TeamUpdate, TeamResponse
from ..services.team_service import TeamService

router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("/", response_model=List[TeamResponse])
def get_teams(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all teams with pagination"""
    teams = TeamService.get_all(db, skip=skip, limit=limit)
    return teams


@router.get("/{team_id}", response_model=TeamResponse)
def get_team(team_id: int, db: Session = Depends(get_db)):
    """Get a specific team by ID"""
    team = TeamService.get_by_id(db, team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID {team_id} not found"
        )
    return team


@router.post("/", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
def create_team(team_data: TeamCreate, db: Session = Depends(get_db)):
    """Create a new team"""
    team = TeamService.create(db, team_data)
    return team


@router.put("/{team_id}", response_model=TeamResponse)
def update_team(
    team_id: int,
    team_data: TeamUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing team"""
    team = TeamService.update(db, team_id, team_data)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID {team_id} not found"
        )
    return team


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(team_id: int, db: Session = Depends(get_db)):
    """Delete a team (soft delete)"""
    success = TeamService.delete(db, team_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID {team_id} not found"
        )
    return None
