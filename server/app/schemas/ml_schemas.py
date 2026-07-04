from pydantic import BaseModel


class MLPredictionRequest(BaseModel):
    age_ciphertext: list[int]
    glucose_ciphertext: list[int]
    blood_pressure_ciphertext: list[int]
    bmi_ciphertext: list[int]
    insulin_ciphertext: list[int]
    model_name: str = "diabetes-logistic"


class MLPredictionResponse(BaseModel):
    ciphertext: list[int]
    status: str
