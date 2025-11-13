"""
Rugby Atlas - User Schemas
Pydantic models for User API requests/responses
"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """Base User schema"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    avatar_url: Optional[str] = Field(None, max_length=500)


class UserCreate(UserBase):
    """Schema for creating a new User"""
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """Schema for updating an existing User"""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    avatar_url: Optional[str] = Field(None, max_length=500)
    password: Optional[str] = Field(None, min_length=8)


class UserResponse(UserBase):
    """Schema for User API responses"""
    id: int
    is_active: bool
    is_verified: bool
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
