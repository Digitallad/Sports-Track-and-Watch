"""
Rugby Atlas - Sport Schemas
Pydantic models for Sport API requests/responses
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class SportBase(BaseModel):
    """Base Sport schema with common fields"""
    name: str = Field(..., max_length=100)
    code: str = Field(..., max_length=20)
    description: Optional[str] = Field(None, max_length=500)
    is_active: bool = True


class SportCreate(SportBase):
    """Schema for creating a new Sport"""
    pass


class SportUpdate(BaseModel):
    """Schema for updating an existing Sport"""
    name: Optional[str] = Field(None, max_length=100)
    code: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None


class SportResponse(SportBase):
    """Schema for Sport API responses"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
