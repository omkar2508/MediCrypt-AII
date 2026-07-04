from uuid import uuid4

import logging
from sqlalchemy.orm import Session

from app.fhe_compute.concrete_backend import ConcretePythonEngine
from app.fhe_compute.serialization import (
    deserialize_ciphertext,
    serialize_ciphertext,
)

from app.fhe_compute.primitives.encrypted_medical_risk import (
    encrypted_medical_risk_score,
)

from app.models.encrypted_record import EncryptedRecord
from app.schemas.medical_schemas import (
    MedicalRecordRequest,
    MedicalRecordResponse,
    MedicalRiskScoreRequest,
    MedicalRiskScoreResponse,
)
from app.services.audit_service import AuditService

logger = logging.getLogger(__name__)


class MedicalService:

    def __init__(self, db: Session, audit_service: AuditService):
        self.db = db
        self.audit_service = audit_service
        self.engine = ConcretePythonEngine()

    def create_record(
        self,
        payload: MedicalRecordRequest,
    ) -> MedicalRecordResponse:

        logger.info("Creating encrypted medical record: key_id=%s", payload.key_id)

        ciphertext_blob = bytes(payload.ciphertext_payload)
        record = EncryptedRecord(
            owner_id="anonymous",
            patient_id=payload.record_handle or "anonymous",
            key_id=payload.key_id,
            ciphertext_blob=ciphertext_blob,
            prediction_status="pending",
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)

        self.audit_service.record_event(
            "Medical Record Created",
            actor=None,
            status="success",
            details=f"record_id={record.id}",
        )

        return MedicalRecordResponse(
            record_id=record.id,
            status="created",
        )

    def score_risk(
        self,
        payload: MedicalRiskScoreRequest,
    ) -> MedicalRiskScoreResponse:

        age = deserialize_ciphertext(payload.age_ciphertext)
        glucose = deserialize_ciphertext(payload.glucose_ciphertext)
        bp = deserialize_ciphertext(payload.blood_pressure_ciphertext)
        bmi = deserialize_ciphertext(payload.bmi_ciphertext)
        insulin = deserialize_ciphertext(payload.insulin_ciphertext)

        encrypted_score = encrypted_medical_risk_score(
            self.engine,
            age,
            glucose,
            bp,
            bmi,
            insulin,
        )

        return MedicalRiskScoreResponse(
            risk_score_ciphertext=serialize_ciphertext(encrypted_score),
            status="completed",
        )