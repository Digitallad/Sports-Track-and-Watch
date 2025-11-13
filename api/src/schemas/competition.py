"""
Rugby Atlas - Competition Schemas
Pydantic models for Competition API requests/responses
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CompetitionBase(BaseModel):
    """Base Competition schema"""
    name: str = Field(..., max_length=200)
    code: str = Field(..., max_length=50)
    sport_id: int
    governing_body_id: Optional[int] = None
    tier: Optional[str] = Field(None, max_length=50)
    format: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    logo_url: Optional[str] = Field(None, max_length=500)
    is_active: bool = True


class CompetitionCreate(CompetitionBase):
    """Schema for creating a new Competition"""
    pass


class CompetitionUpdate(BaseModel):
    """Schema for updating an existing Competition"""
    name: Optional[str] = Field(None, max_length=200)
    code: Optional[str] = Field(None, max_length=50)
    sport_id: Optional[int] = None
    governing_body_id: Optional[int] = None
    tier: Optional[str] = Field(None, max_length=50)
    format: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    logo_url: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None


class CompetitionResponse(CompetitionBase):
    """Schema for Competition API responses"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
