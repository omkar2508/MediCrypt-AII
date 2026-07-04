from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDMixin


class SessionRecord(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "sessions"

    user_id: Mapped[str] = mapped_column(String(36), nullable=False)
    token: Mapped[str] = mapped_column(String(512), nullable=False)
