from app.schemas.encryption_schemas import CiphertextUploadRequest
from app.schemas.prediction_schemas import PredictionRequest
from app.services.encryption_service import EncryptionService
from app.services.prediction_service import PredictionService


def test_prediction_service_returns_completed_ciphertext() -> None:
    encryption_service = EncryptionService()
    handle = encryption_service.store_ciphertext(
        CiphertextUploadRequest(handle=None, payload=[1, 2, 3], key_id="demo-key")
    ).handle

    response = PredictionService().run_prediction(PredictionRequest(ciphertext_handle=handle))
    assert response.status == "completed"
    assert response.ciphertext
