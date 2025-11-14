"""Health check endpoint."""

from fastapi import APIRouter
import torch

from app.core.config import settings
from app.models.schemas import HealthCheck

router = APIRouter()


@router.get("/health", response_model=HealthCheck)
async def health_check():
    """
    Check the health status of the API.

    Returns:
        HealthCheck: Current health status including model availability
    """
    # Check if CUDA is available
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # TODO: Check if model is actually loaded
    model_loaded = False  # Will be updated when we implement model loading

    return HealthCheck(
        status="healthy",
        version=settings.VERSION,
        model_loaded=model_loaded,
        device=device,
    )
