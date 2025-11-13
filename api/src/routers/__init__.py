"""
Rugby Atlas - API Routers
FastAPI route definitions
"""
from .health import router as health_router
from .teams import router as teams_router
from .competitions import router as competitions_router
from .fixtures import router as fixtures_router
from .rights import router as rights_router
from .users import router as users_router

__all__ = [
    "health_router",
    "teams_router",
    "competitions_router",
    "fixtures_router",
    "rights_router",
    "users_router",
]
