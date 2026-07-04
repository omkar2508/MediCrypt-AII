import logging

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_current_user, get_db
from app.services.history_service import HistoryService
from app.schemas.prediction_history_schemas import (
    PredictionDetailResponse,
    PredictionHistoryListResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/prediction", tags=["prediction"])


@router.get("/history", response_model=PredictionHistoryListResponse)
def get_prediction_history(
    record_id: str | None = None,
    current_user: str = Depends(get_current_user),
    db=Depends(get_db),
) -> PredictionHistoryListResponse:
    service = HistoryService(db=db)
    return service.get_history(record_id)


@router.get("/{prediction_id}", response_model=PredictionDetailResponse)
def get_prediction(prediction_id: str, current_user: str = Depends(get_current_user), db=Depends(get_db)) -> PredictionDetailResponse:
    service = HistoryService(db=db)
    try:
        return service.get_prediction(prediction_id)
    except KeyError as exc:
        logger.warning("Prediction not found: %s", exc)
        raise HTTPException(status_code=404, detail=str(exc)) from exc
