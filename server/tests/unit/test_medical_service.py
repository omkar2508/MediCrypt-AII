from app.schemas.medical_schemas import MedicalRiskScoreRequest
from app.services.medical_service import MedicalService


def test_medical_service_returns_encrypted_risk_score() -> None:
    response = MedicalService().score_risk(
        MedicalRiskScoreRequest(
            age_ciphertext=[54],
            glucose_ciphertext=[168],
            blood_pressure_ciphertext=[92],
            bmi_ciphertext=[31],
            insulin_ciphertext=[27],
        )
    )

    assert response.status == "completed"
    assert response.risk_score_ciphertext