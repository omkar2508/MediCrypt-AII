import logging

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_medical_service
from app.schemas.medical_schemas import (
    MedicalRecordRequest,
    MedicalRecordResponse,
    MedicalRiskScoreRequest,
    MedicalRiskScoreResponse,
)
from app.services.medical_service import MedicalService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/medical", tags=["Medical"])


@router.post("", response_model=MedicalRecordResponse)
def create_record(
    payload: MedicalRecordRequest,
    medical_service: MedicalService = Depends(get_medical_service),
):
    try:
        return medical_service.create_record(payload)
    except Exception as exc:
        logger.exception("Failed to create medical record")
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@router.post("/score", response_model=MedicalRiskScoreResponse)
def score_risk(
    payload: MedicalRiskScoreRequest,
    medical_service: MedicalService = Depends(get_medical_service),
):
    try:
        return medical_service.score_risk(payload)
    except Exception as exc:
        logger.exception("Risk scoring failed")
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )