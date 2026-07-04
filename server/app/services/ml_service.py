from __future__ import annotations

import logging

from app.fhe_compute.concrete_backend import ConcretePythonEngine
from app.fhe_compute.model_weights import FEATURE_NAMES
from app.fhe_compute.primitives.encrypted_logistic_regression import encrypted_logistic_regression
from app.fhe_compute.serialization import deserialize_ciphertext, serialize_ciphertext
from app.schemas.ml_schemas import MLPredictionRequest, MLPredictionResponse

logger = logging.getLogger(__name__)


class MLService:
    def __init__(self) -> None:
        self.engine = ConcretePythonEngine()

    def predict_diabetes_risk(self, payload: MLPredictionRequest) -> MLPredictionResponse:
        encrypted_features = [
            deserialize_ciphertext(payload.age_ciphertext),
            deserialize_ciphertext(payload.glucose_ciphertext),
            deserialize_ciphertext(payload.blood_pressure_ciphertext),
            deserialize_ciphertext(payload.bmi_ciphertext),
            deserialize_ciphertext(payload.insulin_ciphertext),
        ]

        if payload.model_name != "diabetes-logistic":
            raise ValueError(f"unsupported model_name: {payload.model_name}")

        logger.info("Running encrypted diabetes risk prediction with model %s", payload.model_name)
        result_ciphertext = encrypted_logistic_regression(self.engine, encrypted_features)

        return MLPredictionResponse(ciphertext=serialize_ciphertext(result_ciphertext), status="completed")
