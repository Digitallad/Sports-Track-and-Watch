"""
Rugby Atlas - Pydantic Schemas
Request/response schemas for API endpoints
"""
from .sport import SportBase, SportCreate, SportUpdate, SportResponse
from .competition import CompetitionBase, CompetitionCreate, CompetitionUpdate, CompetitionResponse
from .team import TeamBase, TeamCreate, TeamUpdate, TeamResponse
from .fixture import FixtureBase, FixtureCreate, FixtureUpdate, FixtureResponse
from .user import UserBase, UserCreate, UserUpdate, UserResponse

__all__ = [
    "SportBase",
    "SportCreate",
    "SportUpdate",
    "SportResponse",
    "CompetitionBase",
    "CompetitionCreate",
    "CompetitionUpdate",
    "CompetitionResponse",
    "TeamBase",
    "TeamCreate",
    "TeamUpdate",
    "TeamResponse",
    "FixtureBase",
    "FixtureCreate",
    "FixtureUpdate",
    "FixtureResponse",
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
]
