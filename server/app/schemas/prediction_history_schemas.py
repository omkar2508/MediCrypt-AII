from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class PredictionHistoryResponse(BaseModel):
    id: str
    source_record_id: str
    model_version: str
    execution_time_ms: int
    ciphertext_handle: str
    status: str
    created_at: datetime


class PredictionDetailResponse(PredictionHistoryResponse):
    result_blob: list[int]


class PredictionHistoryListResponse(BaseModel):
    history: list[PredictionHistoryResponse]
