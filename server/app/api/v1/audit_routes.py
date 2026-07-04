import logging

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, get_db
from app.services.audit_service import AuditService
from app.schemas.audit_schemas import AuditLogsResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("/logs", response_model=AuditLogsResponse)
def get_audit_logs(current_user: str = Depends(get_current_user), db=Depends(get_db)) -> AuditLogsResponse:
    service = AuditService(db)
    records = service.list_events()
    logger.info("Audit logs retrieved by %s", current_user)
    return AuditLogsResponse(logs=[service.to_response(event) for event in records])
