from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin


class SharedMedicalRecord(UUIDMixin, Base):
    __tablename__ = "shared_medical_records"

    record_id: Mapped[str] = mapped_column(String(36), ForeignKey("encrypted_records.id"), nullable=False)
    shared_with_user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    permission: Mapped[str] = mapped_column(String(50), nullable=False, default="view")

    record = relationship("EncryptedRecord", back_populates="shared_records")
    shared_with_user = relationship("User", back_populates="shared_records")
