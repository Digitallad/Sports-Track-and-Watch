"""
Rugby Atlas - Fixture Schemas
Pydantic models for Fixture API requests/responses
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class FixtureBase(BaseModel):
    """Base Fixture schema"""
    season_id: int
    home_team_id: int
    away_team_id: int
    venue_id: Optional[int] = None
    match_date: datetime
    round: Optional[str] = Field(None, max_length=50)
    status: str = Field(default="scheduled", max_length=50)
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    external_id: Optional[str] = Field(None, max_length=200)
    source: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None
    is_active: bool = True


class FixtureCreate(FixtureBase):
    """Schema for creating a new Fixture"""
    pass


class FixtureUpdate(BaseModel):
    """Schema for updating an existing Fixture"""
    season_id: Optional[int] = None
    home_team_id: Optional[int] = None
    away_team_id: Optional[int] = None
    venue_id: Optional[int] = None
    match_date: Optional[datetime] = None
    round: Optional[str] = Field(None, max_length=50)
    status: Optional[str] = Field(None, max_length=50)
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    external_id: Optional[str] = Field(None, max_length=200)
    source: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class FixtureResponse(FixtureBase):
    """Schema for Fixture API responses"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
