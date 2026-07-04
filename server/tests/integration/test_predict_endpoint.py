from fastapi.testclient import TestClient

from app.main import app


def test_predict_endpoint() -> None:
    client = TestClient(app)
    response = client.post("/api/predict", json={"ciphertext_handle": "abc"})
    assert response.status_code == 200
    assert response.json()["status"] == "queued"
