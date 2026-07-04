import logging

from fastapi import APIRouter

from app.config.constants import API_VERSION

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/system", tags=["system"])


@router.get("/health")
def health() -> dict[str, str]:
    logger.debug("System health check requested")
    return {"status": "healthy"}


@router.get("/status")
def status() -> dict[str, str]:
    logger.debug("System status requested for version %s", API_VERSION)
    return {"status": "ok", "version": API_VERSION}
