from __future__ import annotations

import logging
from time import perf_counter

from sqlalchemy.orm import Session

from app.models.encrypted_record import EncryptedRecord
from app.models.prediction import Prediction
from app.schemas.prediction_history_schemas import (
    PredictionDetailResponse,
    PredictionHistoryListResponse,
    PredictionHistoryResponse,
)
from app.schemas.prediction_schemas import PredictionRequest, PredictionResponse
from app.services.audit_service import AuditService
from app.services.encryption_service import EncryptionService

logger = logging.getLogger(__name__)


class HistoryService:
    def __init__(self, db: Session, audit_service: AuditService | None = None) -> None:
        self.db = db
        self.audit_service = audit_service
        self.encryption_service = EncryptionService()

    def _audit(self, action: str, status: str, details: str = "") -> None:
        if self.audit_service:
            self.audit_service.record_event(action, actor=None, status=status, details=details)

    def record_prediction(self, payload: PredictionRequest) -> PredictionResponse:
        if not payload.ciphertext_handle.strip():
            raise ValueError("ciphertext_handle must not be empty")

        ciphertext = self.encryption_service.load_ciphertext(payload.ciphertext_handle)
        encrypted_result = self.db.scalar(self.db.select(EncryptedRecord).where(EncryptedRecord.id == payload.ciphertext_handle))

        start = perf_counter()
        # placeholder for evaluate_prediction call
        end = perf_counter()
        execution_time_ms = int((end - start) * 1000)

        prediction = Prediction(
            source_record_id=payload.ciphertext_handle,
            result_blob=ciphertext,
            model_version="diabetes-logistic",
            execution_time_ms=execution_time_ms,
            ciphertext_handle=payload.ciphertext_handle,
            status="completed",
        )
        self.db.add(prediction)
        self.db.commit()
        self.db.refresh(prediction)
        self._audit("Prediction Requested", "success", f"prediction_id={prediction.id}")

        return PredictionResponse(ciphertext=list(prediction.result_blob), status=prediction.status)

    def get_history(self, record_id: str | None = None) -> PredictionHistoryListResponse:
        query = self.db.query(Prediction)
        if record_id:
            query = query.filter(Prediction.source_record_id == record_id)
        history = query.order_by(Prediction.created_at.desc()).all()
        self._audit("Retrieve Prediction History", "success", f"record_id={record_id}")
        return PredictionHistoryListResponse(
            history=[
                PredictionHistoryResponse(
                    id=entry.id,
                    source_record_id=entry.source_record_id,
                    model_version=entry.model_version,
                    execution_time_ms=entry.execution_time_ms,
                    ciphertext_handle=entry.ciphertext_handle,
                    status=entry.status,
                    created_at=entry.created_at,
                )
                for entry in history
            ]
        )

    def get_prediction(self, prediction_id: str) -> PredictionDetailResponse:
        prediction = self.db.get(Prediction, prediction_id)
        if prediction is None:
            self._audit("Retrieve Prediction", "failure", f"prediction_id={prediction_id}")
            raise KeyError(f"Prediction not found: {prediction_id}")

        self._audit("Retrieve Prediction", "success", f"prediction_id={prediction_id}")
        return PredictionDetailResponse(
            id=prediction.id,
            source_record_id=prediction.source_record_id,
            model_version=prediction.model_version,
            execution_time_ms=prediction.execution_time_ms,
            ciphertext_handle=prediction.ciphertext_handle,
            status=prediction.status,
            created_at=prediction.created_at,
            result_blob=list(prediction.result_blob),
        )
