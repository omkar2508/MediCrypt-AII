from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_prediction_service
from app.schemas.prediction_schemas import PredictionRequest, PredictionResponse
from app.services.prediction_service import PredictionService

router = APIRouter(prefix="/predict", tags=["predict"])


@router.post("", response_model=PredictionResponse)
def predict(payload: PredictionRequest, prediction_service: PredictionService = Depends(get_prediction_service)) -> PredictionResponse:
    try:
        return prediction_service.run_prediction(payload)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
