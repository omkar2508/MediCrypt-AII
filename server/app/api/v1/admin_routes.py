from fastapi import APIRouter, Depends

from app.api.deps import get_audit_service
from app.services.audit_service import AuditService

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/audit-log")
def get_audit_log(audit_service: AuditService = Depends(get_audit_service)) -> dict[str, object]:
    return {"entries": audit_service.list_events()}
