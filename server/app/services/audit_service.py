from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


class AuditService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def record_event(self, action: str, actor: str | None = None, status: str = "success", ip_address: str | None = None, details: str = "") -> AuditLog:
        entry = AuditLog(actor=actor, action=action, status=status, ip_address=ip_address, details=details)
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        return entry

    def list_events(self) -> list[AuditLog]:
        return self.db.query(AuditLog).order_by(AuditLog.created_at.desc()).all()

    def to_response(self, entry: AuditLog) -> dict[str, object]:
        return {
            "id": entry.id,
            "actor": entry.actor,
            "action": entry.action,
            "status": entry.status,
            "ip_address": entry.ip_address,
            "details": entry.details,
            "created_at": entry.created_at,
        }
