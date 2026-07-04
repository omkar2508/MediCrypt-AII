from fastapi import APIRouter

from app.api.v1 import (
    audit_routes,
    encryption_routes,
    history_routes,
    medical_routes,
    ml_routes,
    predict_routes,
    record_routes,
    system_routes,
)

router = APIRouter(prefix="/api")
router.include_router(encryption_routes.router)
router.include_router(predict_routes.router)
router.include_router(medical_routes.router)
router.include_router(record_routes.router)
router.include_router(history_routes.router)
router.include_router(audit_routes.router)
router.include_router(ml_routes.router)
router.include_router(system_routes.router)
