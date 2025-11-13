"""
Rugby Atlas - User Service
Business logic for user management
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from ..core.logging import get_logger

logger = get_logger(__name__)


class UserService:
    """Service class for user operations"""
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        logger.info(f"Fetching users: skip={skip}, limit={limit}")
        return db.query(User).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get a user by ID"""
        logger.info(f"Fetching user with ID: {user_id}")
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        """Get a user by email"""
        logger.info(f"Fetching user with email: {email}")
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_by_username(db: Session, username: str) -> Optional[User]:
        """Get a user by username"""
        logger.info(f"Fetching user with username: {username}")
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def create(db: Session, user_data: UserCreate) -> User:
        """Create a new user"""
        logger.info(f"Creating new user: {user_data.email}")
        
        # In production, hash the password properly
        # For now, this is a placeholder
        hashed_password = f"hashed_{user_data.password}"
        
        user_dict = user_data.model_dump(exclude={"password"})
        user = User(**user_dict, hashed_password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"User created successfully with ID: {user.id}")
        return user
    
    @staticmethod
    def update(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update an existing user"""
        logger.info(f"Updating user with ID: {user_id}")
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.warning(f"User with ID {user_id} not found")
            return None
        
        update_data = user_data.model_dump(exclude_unset=True, exclude={"password"})
        for key, value in update_data.items():
            setattr(user, key, value)
        
        # Handle password update separately
        if user_data.password:
            user.hashed_password = f"hashed_{user_data.password}"
        
        db.commit()
        db.refresh(user)
        logger.info(f"User {user_id} updated successfully")
        return user
    
    @staticmethod
    def delete(db: Session, user_id: int) -> bool:
        """Delete a user (soft delete)"""
        logger.info(f"Deleting user with ID: {user_id}")
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.warning(f"User with ID {user_id} not found")
            return False
        
        user.is_active = False
        db.commit()
        logger.info(f"User {user_id} deleted successfully")
        return True
