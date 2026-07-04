from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class User(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    role: Mapped[str] = mapped_column(String(50), default="user", nullable=False)

    refresh_tokens = relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    shared_records = relationship(
        "SharedMedicalRecord",
        back_populates="shared_with_user",
        cascade="all, delete-orphan",
    )
