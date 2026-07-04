from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class AuditLogResponse(BaseModel):
    id: str
    actor: str | None
    action: str
    status: str
    ip_address: str | None
    details: str
    created_at: datetime


class AuditLogsResponse(BaseModel):
    logs: list[AuditLogResponse]
