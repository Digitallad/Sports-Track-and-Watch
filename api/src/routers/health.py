"""
Rugby Atlas - Health Check Router
Simple health check endpoint
"""
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
@router.get("/healthz")
def health_check():
    """
    Health check endpoint.
    Returns a simple status message.
    """
    return {"status": "ok", "service": "Rugby Atlas API"}
