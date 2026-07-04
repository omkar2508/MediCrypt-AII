from sqlalchemy import ForeignKey, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Prediction(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "predictions"

    source_record_id: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )

    result_blob: Mapped[bytes] = mapped_column(
        LargeBinary,
        nullable=False,
    )

    model_version: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    execution_time_ms: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
    )

    ciphertext_handle: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="completed",
    )