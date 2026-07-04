from __future__ import annotations

import logging
from time import perf_counter
import base64

from sqlalchemy.orm import Session

from app.fhe_compute.dev_backend import DevPythonEngine, derive_evaluation_key
from app.fhe_compute.serialization import serialize_ciphertext
from app.models.encrypted_record import EncryptedRecord
from app.models.prediction import Prediction
from app.models.public_evaluation_key import PublicEvaluationKey
from app.schemas.prediction_schemas import PredictionRequest, PredictionResponse
from app.services.audit_service import AuditService
from app.services.encryption_service import EncryptionService

logger = logging.getLogger(__name__)


class PredictionService:
    def __init__(self, db: Session, audit_service: AuditService, encryption_service: EncryptionService) -> None:
        self.db = db
        self.engine = DevPythonEngine()
        self.encryption_service = encryption_service
        self.audit_service = audit_service

    def run_prediction(self, payload: PredictionRequest) -> PredictionResponse:
        if not payload.record_id and not payload.ciphertext_handle:
            raise ValueError("either record_id or ciphertext_handle must be provided")

        record = None
        ciphertext_source = payload.ciphertext_handle
        key_id = None
        if payload.record_id:
            record = self.db.get(EncryptedRecord, payload.record_id)
            if record is None or record.is_deleted:
                raise KeyError(f"Record not found: {payload.record_id}")
            ciphertext_source = payload.record_id
            ciphertext = record.ciphertext_blob
            key_id = record.key_id
        else:
            ciphertext = self.encryption_service.load_ciphertext(payload.ciphertext_handle)
            key_id = self.encryption_service.get_ciphertext_key_id(payload.ciphertext_handle)

        if not key_id:
            raise ValueError("Cannot determine key_id for ciphertext")

        key_entry = self.db.query(PublicEvaluationKey).filter(PublicEvaluationKey.key_id == key_id).first()
        if key_entry is not None:
            key_material = base64.b64decode(key_entry.key_material)
        else:
            logger.warning("Evaluation key %s not found, using derived fallback key material", key_id)
            key_material = derive_evaluation_key(key_id.encode("utf-8"))

        start = perf_counter()
        encrypted_result = self.engine.evaluate_prediction(ciphertext, key_material=key_material)
        execution_time_ms = int((perf_counter() - start) * 1000)

        prediction = Prediction(
            source_record_id=payload.record_id or payload.ciphertext_handle,
            result_blob=bytes(encrypted_result),
            model_version=payload.model_name,
            execution_time_ms=execution_time_ms,
            ciphertext_handle=ciphertext_source,
            status="completed",
        )
        self.db.add(prediction)

        if record is not None:
            record.prediction_status = "completed"
            record.prediction_id = prediction.id
            self.db.add(record)

        self.db.commit()
        self.db.refresh(prediction)

        self.audit_service.record_event("Prediction Completed", actor=None, status="success", details=f"prediction_id={prediction.id}")

        logger.info("Ran encrypted prediction and stored history %s", prediction.id)
        return PredictionResponse(ciphertext=serialize_ciphertext(prediction.result_blob), status=prediction.status)
