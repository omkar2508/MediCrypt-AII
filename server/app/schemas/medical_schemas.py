from typing import Optional

from pydantic import BaseModel, Field


class MedicalRecordRequest(BaseModel):
    record_handle: Optional[str] = None
    ciphertext_payload: list[int] = Field(..., min_items=1)
    key_id: str = Field(..., min_length=1)


class MedicalRecordResponse(BaseModel):
    record_id: str
    status: str


class MedicalRiskScoreRequest(BaseModel):
    age_ciphertext: list[int]
    glucose_ciphertext: list[int]
    blood_pressure_ciphertext: list[int]
    bmi_ciphertext: list[int]
    insulin_ciphertext: list[int]


class MedicalRiskScoreResponse(BaseModel):
    risk_score_ciphertext: list[int]
    status: str