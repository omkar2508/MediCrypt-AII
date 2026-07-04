from app.schemas.ml_schemas import MLPredictionRequest
from app.services.ml_service import MLService


def test_ml_service_predicts_diabetes_risk() -> None:
    request = MLPredictionRequest(
        age_ciphertext=[54],
        glucose_ciphertext=[168],
        blood_pressure_ciphertext=[92],
        bmi_ciphertext=[31],
        insulin_ciphertext=[27],
    )

    response = MLService().predict_diabetes_risk(request)

    assert response.status == "completed"
    assert isinstance(response.ciphertext, list)
    assert response.ciphertext
