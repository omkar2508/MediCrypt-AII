from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class MedicalRecordUploadRequest(BaseModel):
    patient_id: str = Field(..., min_length=1)
    key_id: str = Field(..., min_length=1)
    ciphertext_blob: list[int]
    model_version: str = Field("v1", min_length=1)


class MedicalRecordUpdateRequest(BaseModel):
    model_version: str | None = None
    prediction_status: str | None = None


class MedicalRecordResponse(BaseModel):
    id: str
    patient_id: str
    key_id: str
    model_version: str
    prediction_status: str
    prediction_id: str | None
    created_at: datetime
    deleted_at: datetime | None


class MedicalRecordDetailResponse(MedicalRecordResponse):
    ciphertext_blob: list[int]


class MedicalRecordListResponse(BaseModel):
    records: list[MedicalRecordResponse]
