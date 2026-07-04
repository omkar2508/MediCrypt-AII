from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDMixin


class AuditLog(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "audit_logs"

    actor: Mapped[str | None] = mapped_column(String(255), nullable=True)
    action: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="success")
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    details: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
