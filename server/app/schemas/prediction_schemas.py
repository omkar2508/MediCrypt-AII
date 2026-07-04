from pydantic import BaseModel, field_validator


class PredictionRequest(BaseModel):
    ciphertext_handle: str | None = None
    record_id: str | None = None
    model_name: str = "default"

    @field_validator("ciphertext_handle", mode="after")
    def at_least_one_identifier(cls, value: str | None, info: dict) -> str | None:
        if not value and not info.data.get("record_id"):
            raise ValueError("either ciphertext_handle or record_id must be provided")
        return value


class PredictionResponse(BaseModel):
    ciphertext: list[int]
    status: str
