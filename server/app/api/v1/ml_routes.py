import logging

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_ml_service
from app.schemas.ml_schemas import MLPredictionRequest, MLPredictionResponse
from app.services.ml_service import MLService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ml", tags=["ml"])


@router.post("/predict", response_model=MLPredictionResponse)
def predict(payload: MLPredictionRequest, ml_service: MLService = Depends(get_ml_service)) -> MLPredictionResponse:
    try:
        return ml_service.predict_diabetes_risk(payload)
    except (TypeError, ValueError) as exc:
        logger.warning("Invalid ML prediction request: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc
