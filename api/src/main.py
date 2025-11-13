"""
Rugby Atlas - Main Application
FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .core.db import Base, engine
from .core.logging import setup_logging, get_logger
from .routers import (
    health_router,
    teams_router,
    competitions_router,
    fixtures_router,
    rights_router,
    users_router,
)

# Initialize logging
setup_logging()
logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Rugby Atlas - Global rugby broadcast rights and fixture intelligence platform",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    """Application startup handler - creates database tables"""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    
    # Create database tables
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")


@app.on_event("shutdown")
def shutdown():
    """Application shutdown handler"""
    logger.info("Shutting down Rugby Atlas API")


# Include routers
app.include_router(health_router)
app.include_router(teams_router, prefix=settings.API_PREFIX)
app.include_router(competitions_router, prefix=settings.API_PREFIX)
app.include_router(fixtures_router, prefix=settings.API_PREFIX)
app.include_router(rights_router, prefix=settings.API_PREFIX)
app.include_router(users_router, prefix=settings.API_PREFIX)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
    }
