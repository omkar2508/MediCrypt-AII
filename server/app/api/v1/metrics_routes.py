import logging

from fastapi import APIRouter
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/")
def metrics() -> tuple[bytes, str]:
    logger.debug("Metrics endpoint requested")
    return generate_latest(), CONTENT_TYPE_LATEST
