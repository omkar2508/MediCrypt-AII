from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin


class RefreshToken(UUIDMixin, Base):
    __tablename__ = "refresh_tokens"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    token: Mapped[str] = mapped_column(String(512), nullable=False, unique=True)
    expired_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    user = relationship("User", back_populates="refresh_tokens")
