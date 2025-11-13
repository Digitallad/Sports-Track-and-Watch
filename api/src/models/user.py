"""
Rugby Atlas - User Models
User, UserLocation, UserPreference, NotificationSubscription
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from ..core.db import Base


class User(Base):
    """User entity"""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    
    # Profile
    first_name = Column(String(100))
    last_name = Column(String(100))
    avatar_url = Column(String(500))
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    last_login = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    locations = relationship("UserLocation", back_populates="user")
    preferences = relationship("UserPreference", back_populates="user")
    subscriptions = relationship("NotificationSubscription", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', username='{self.username}')>"


class UserLocation(Base):
    """User location history for rights personalization"""
    
    __tablename__ = "user_locations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    territory_id = Column(Integer, ForeignKey("territories.id"), nullable=False)
    
    # Location details
    latitude = Column(String(50))
    longitude = Column(String(50))
    ip_address = Column(String(50))
    
    # Metadata
    is_current = Column(Boolean, default=True)
    detected_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="locations")
    territory = relationship("Territory", back_populates="user_locations")
    
    def __repr__(self):
        return f"<UserLocation(id={self.id}, user_id={self.user_id}, territory_id={self.territory_id})>"


class UserPreference(Base):
    """User preferences for teams, competitions, etc."""
    
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Preference details
    preference_type = Column(String(50), nullable=False)  # "favorite_team", "favorite_competition"
    entity_type = Column(String(50), nullable=False)  # "team", "competition"
    entity_id = Column(Integer, nullable=False)
    
    # Metadata
    priority = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="preferences")
    
    def __repr__(self):
        return f"<UserPreference(id={self.id}, user_id={self.user_id}, type='{self.preference_type}')>"


class NotificationSubscription(Base):
    """User notification subscriptions"""
    
    __tablename__ = "notification_subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Subscription details
    subscription_type = Column(String(50), nullable=False)  # "fixture_reminder", "score_update"
    entity_type = Column(String(50))  # "team", "competition", "fixture"
    entity_id = Column(Integer)
    
    # Notification settings
    notify_email = Column(Boolean, default=True)
    notify_push = Column(Boolean, default=False)
    advance_minutes = Column(Integer, default=60)  # For reminders
    
    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="subscriptions")
    
    def __repr__(self):
        return f"<NotificationSubscription(id={self.id}, user_id={self.user_id}, type='{self.subscription_type}')>"
