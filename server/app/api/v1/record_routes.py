import logging

from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.deps import get_current_user, get_db
from app.services.record_service import RecordService
from app.schemas.medical_record_schemas import (
    MedicalRecordDetailResponse,
    MedicalRecordListResponse,
    MedicalRecordResponse,
    MedicalRecordUpdateRequest,
    MedicalRecordUploadRequest,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/medical", tags=["medical"])


@router.post("/upload", response_model=MedicalRecordResponse)
def upload_record(
    payload: MedicalRecordUploadRequest,
    current_user: str = Depends(get_current_user),
    db=Depends(get_db),
) -> MedicalRecordResponse:
    service = RecordService(db=db, actor=current_user)
    try:
        return service.upload_record(payload)
    except ValueError as exc:
        logger.warning("Invalid medical record upload: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{record_id}", response_model=MedicalRecordDetailResponse)
def get_record(record_id: str, current_user: str = Depends(get_current_user), db=Depends(get_db)) -> MedicalRecordDetailResponse:
    service = RecordService(db=db, actor=current_user)
    try:
        return service.get_record(record_id)
    except KeyError as exc:
        logger.warning("Medical record not found: %s", exc)
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/list", response_model=MedicalRecordListResponse)
def list_records(
    patient_id: str | None = Query(None, alias="patient"),
    current_user: str = Depends(get_current_user),
    db=Depends(get_db),
) -> MedicalRecordListResponse:
    service = RecordService(db=db, actor=current_user)
    return service.list_records(patient_id)


@router.delete("/{record_id}", response_model=MedicalRecordResponse)
def delete_record(record_id: str, current_user: str = Depends(get_current_user), db=Depends(get_db)) -> MedicalRecordResponse:
    service = RecordService(db=db, actor=current_user)
    try:
        return service.soft_delete_record(record_id)
    except KeyError as exc:
        logger.warning("Medical record delete failed: %s", exc)
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.patch("/{record_id}", response_model=MedicalRecordResponse)
def update_record(
    record_id: str,
    payload: MedicalRecordUpdateRequest,
    current_user: str = Depends(get_current_user),
    db=Depends(get_db),
) -> MedicalRecordResponse:
    service = RecordService(db=db, actor=current_user)
    try:
        return service.update_record_metadata(record_id, payload)
    except KeyError as exc:
        logger.warning("Medical record metadata update failed: %s", exc)
        raise HTTPException(status_code=404, detail=str(exc)) from exc
