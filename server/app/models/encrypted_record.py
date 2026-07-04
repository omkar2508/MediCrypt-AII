from datetime import datetime

from sqlalchemy import Boolean, DateTime, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class EncryptedRecord(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "encrypted_records"

    owner_id: Mapped[str] = mapped_column(String(36), nullable=False)
    patient_id: Mapped[str] = mapped_column(String(64), nullable=False)
    key_id: Mapped[str] = mapped_column(String(64), nullable=False)
    prediction_id: Mapped[str | None] = mapped_column(String(36), nullable=True)

    ciphertext_blob: Mapped[bytes] = mapped_column(
        LargeBinary,
        nullable=False,
    )

    model_version: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        default="v1",
    )

    prediction_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending",
    )

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )