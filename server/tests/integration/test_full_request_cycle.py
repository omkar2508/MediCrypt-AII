from fastapi.testclient import TestClient

from app.main import app


def test_health_and_medical_score_cycle() -> None:
    client = TestClient(app)
    health_response = client.get("/api/system/health")
    assert health_response.status_code == 200

    medical_response = client.post(
        "/api/medical/score",
        json={
            "age_ciphertext": [54],
            "glucose_ciphertext": [168],
            "blood_pressure_ciphertext": [92],
            "bmi_ciphertext": [31],
            "insulin_ciphertext": [27],
        },
    )
    assert medical_response.status_code == 200
    assert medical_response.json()["status"] == "completed"
    assert medical_response.json()["risk_score_ciphertext"]
