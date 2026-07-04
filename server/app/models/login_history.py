from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin


class LoginHistory(UUIDMixin, Base):
    __tablename__ = "login_history"

    user_id: Mapped[str] = mapped_column(String(36), nullable=False)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
