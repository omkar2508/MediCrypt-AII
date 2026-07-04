from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin


class Permission(UUIDMixin, Base):
    __tablename__ = "permissions"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
