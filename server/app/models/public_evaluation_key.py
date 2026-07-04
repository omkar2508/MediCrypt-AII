from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin


class PublicEvaluationKey(UUIDMixin, Base):
    __tablename__ = "public_evaluation_keys"

    owner_id: Mapped[str] = mapped_column(String(36), nullable=False)
    key_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    key_material: Mapped[str] = mapped_column(String(2048), nullable=False)
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="v1")
    revoked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
