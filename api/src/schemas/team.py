"""
Rugby Atlas - Team Schemas
Pydantic models for Team API requests/responses
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TeamBase(BaseModel):
    """Base Team schema"""
    name: str = Field(..., max_length=200)
    short_name: Optional[str] = Field(None, max_length=100)
    code: Optional[str] = Field(None, max_length=20)
    type: Optional[str] = Field(None, max_length=50)
    country: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=100)
    logo_url: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    is_active: bool = True


class TeamCreate(TeamBase):
    """Schema for creating a new Team"""
    pass


class TeamUpdate(BaseModel):
    """Schema for updating an existing Team"""
    name: Optional[str] = Field(None, max_length=200)
    short_name: Optional[str] = Field(None, max_length=100)
    code: Optional[str] = Field(None, max_length=20)
    type: Optional[str] = Field(None, max_length=50)
    country: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=100)
    logo_url: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    is_active: Optional[bool] = None


class TeamResponse(TeamBase):
    """Schema for Team API responses"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
