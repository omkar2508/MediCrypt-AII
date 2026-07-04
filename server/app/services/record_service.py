from __future__ import annotations

import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.encrypted_record import EncryptedRecord
from app.schemas.medical_record_schemas import (
    MedicalRecordDetailResponse,
    MedicalRecordListResponse,
    MedicalRecordResponse,
    MedicalRecordUpdateRequest,
    MedicalRecordUploadRequest,
)
from app.services.audit_service import AuditService

logger = logging.getLogger(__name__)


class RecordService:
    def __init__(self, db: Session, actor: str | None = None, ip_address: str | None = None) -> None:
        self.db = db
        self.audit = AuditService(db)
        self.actor = actor
        self.ip_address = ip_address

    def _audit(self, action: str, status: str, details: str = "") -> None:
        self.audit.record_event(action, actor=self.actor, status=status, ip_address=self.ip_address, details=details)

    def upload_record(self, payload: MedicalRecordUploadRequest) -> MedicalRecordResponse:
        if not payload.patient_id.strip():
            raise ValueError("patient_id must not be empty")
        if not payload.key_id.strip():
            raise ValueError("key_id must not be empty")
        if not payload.ciphertext_blob:
            raise ValueError("ciphertext_blob must not be empty")

        encrypted_blob = bytes(int(value) for value in payload.ciphertext_blob)
        record = EncryptedRecord(
            patient_id=payload.patient_id,
            owner_id=self.actor or "anonymous",
            key_id=payload.key_id,
            ciphertext_blob=encrypted_blob,
            model_version=payload.model_version,
            prediction_status="pending",
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        self._audit("Record Uploaded", "success", f"record_id={record.id}")
        return MedicalRecordResponse(
            id=record.id,
            patient_id=record.patient_id,
            key_id=record.key_id,
            model_version=record.model_version,
            prediction_status=record.prediction_status,
            prediction_id=record.prediction_id,
            created_at=record.created_at,
            deleted_at=record.deleted_at,
        )

    def get_record(self, record_id: str) -> MedicalRecordDetailResponse:
        record = self.db.get(EncryptedRecord, record_id)
        if record is None or record.is_deleted:
            self._audit("Ciphertext Retrieved", "failure", f"record_id={record_id}")
            raise KeyError(f"Record not found: {record_id}")

        self._audit("Ciphertext Retrieved", "success", f"record_id={record_id}")
        return MedicalRecordDetailResponse(
            id=record.id,
            patient_id=record.patient_id,
            key_id=record.key_id,
            model_version=record.model_version,
            prediction_status=record.prediction_status,
            prediction_id=record.prediction_id,
            created_at=record.created_at,
            deleted_at=record.deleted_at,
            ciphertext_blob=list(record.ciphertext_blob),
        )

    def list_records(self, patient_id: str | None = None) -> MedicalRecordListResponse:
        query = self.db.query(EncryptedRecord).filter(EncryptedRecord.is_deleted == False)
        if patient_id:
            query = query.filter(EncryptedRecord.patient_id == patient_id)
        records = query.all()
        self._audit("List Records", "success", f"patient_id={patient_id}")
        return MedicalRecordListResponse(
            records=[
                MedicalRecordResponse(
                    id=record.id,
                    patient_id=record.patient_id,
                    key_id=record.key_id,
                    model_version=record.model_version,
                    prediction_status=record.prediction_status,
                    prediction_id=record.prediction_id,
                    created_at=record.created_at,
                    deleted_at=record.deleted_at,
                )
                for record in records
            ]
        )

    def soft_delete_record(self, record_id: str) -> MedicalRecordResponse:
        record = self.db.get(EncryptedRecord, record_id)
        if record is None or record.is_deleted:
            self._audit("Delete Record", "failure", f"record_id={record_id}")
            raise KeyError(f"Record not found: {record_id}")

        record.is_deleted = True
        record.deleted_at = datetime.now(timezone.utc)
        self.db.add(record)
        self.db.commit()
        self._audit("Delete Record", "success", f"record_id={record_id}")
        return MedicalRecordResponse(
            id=record.id,
            patient_id=record.patient_id,
            key_id=record.key_id,
            model_version=record.model_version,
            prediction_status=record.prediction_status,
            prediction_id=record.prediction_id,
            created_at=record.created_at,
            deleted_at=record.deleted_at,
        )

    def update_record_metadata(self, record_id: str, payload: MedicalRecordUpdateRequest) -> MedicalRecordResponse:
        record = self.db.get(EncryptedRecord, record_id)
        if record is None or record.is_deleted:
            self._audit("Update Metadata", "failure", f"record_id={record_id}")
            raise KeyError(f"Record not found: {record_id}")

        if payload.model_version is not None:
            record.model_version = payload.model_version
        if payload.prediction_status is not None:
            record.prediction_status = payload.prediction_status

        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        self._audit("Update Metadata", "success", f"record_id={record_id}")
        return MedicalRecordResponse(
            id=record.id,
            patient_id=record.patient_id,
            key_id=record.key_id,
            model_version=record.model_version,
            prediction_status=record.prediction_status,
            prediction_id=record.prediction_id,
            created_at=record.created_at,
            deleted_at=record.deleted_at,
        )
