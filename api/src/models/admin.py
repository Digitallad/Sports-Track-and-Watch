"""
Rugby Atlas - Admin User Model
Admin users with elevated permissions
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from datetime import datetime

from ..core.db import Base


class AdminUser(Base):
    """Admin user entity"""
    
    __tablename__ = "admin_users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    
    # Profile
    full_name = Column(String(200))
    
    # Permissions
    role = Column(String(50), default="admin")  # "admin", "super_admin", "moderator"
    permissions = Column(Text)  # JSON string of permissions
    
    # Status
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<AdminUser(id={self.id}, email='{self.email}', role='{self.role}')>"
