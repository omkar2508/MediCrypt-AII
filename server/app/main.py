import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.metrics_routes import router as metrics_router
from app.api.v1.router import router as v1_router
from app.config.logging_config import configure_logging
from app.config.settings import get_settings
from app.middleware.auth_middleware import auth_middleware
from app.middleware.correlation_id import correlation_id_middleware
from app.middleware.error_handler import register_error_handler
from app.middleware.metrics_middleware import metrics_middleware
from app.middleware.rate_limiter import SlidingWindowRateLimiter
from app.middleware.request_logger import request_logging_middleware
from app.middleware.security_middleware import security_middleware
from app.db.migrations import ensure_public_evaluation_keys_table

logger = logging.getLogger(__name__)

configure_logging()
settings = get_settings()

app = FastAPI(title=settings.app_name, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.allowed_origins.split(",")],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Correlation-ID"],
    max_age=settings.cors_max_age,
)

app.middleware("http")(security_middleware)
app.middleware("http")(correlation_id_middleware)
app.middleware("http")(request_logging_middleware)
app.middleware("http")(auth_middleware)
app.middleware("http")(metrics_middleware)
app.middleware("http")(SlidingWindowRateLimiter(limit=settings.rate_limit_requests, window_seconds=settings.rate_limit_window_seconds))

app.include_router(v1_router)
app.include_router(metrics_router)


@app.on_event("startup")
def startup() -> None:
    logger.info("Medicrypt AI server starting up")
    # Ensure important DB tables exist for runtime
    try:
        ensure_public_evaluation_keys_table()
    except Exception:
        logger.exception("Database migrations failed during startup")


@app.on_event("shutdown")
def shutdown() -> None:
    logger.info("Medicrypt AI server shutting down")


@app.get("/")
def root() -> dict[str, str]:
    return {"service": "medicrypt-ai-server", "status": "ok"}
