"""
Rugby Atlas - Core Configuration
Manages application settings using Pydantic Settings
"""
from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/rugby_atlas"
    
    # Application
    APP_NAME: str = "Rugby Atlas API"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    DEBUG: bool = True
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/rugby_atlas.log"
    
    # API
    API_PREFIX: str = "/api/v1"
    
    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Security (placeholder)
    SECRET_KEY: str = "change-me-in-production"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
