from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin


class DoctorPatientMapping(UUIDMixin, Base):
    __tablename__ = "doctor_patient_mappings"

    doctor_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    patient_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)

    doctor = relationship("User", foreign_keys=[doctor_id])
    patient = relationship("User", foreign_keys=[patient_id])
