from __future__ import annotations

import logging

import httpx


logger = logging.getLogger(__name__)


class MedicryptApiClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(base_url=self.base_url, timeout=30.0)

    def close(self) -> None:
        self._client.close()

    def upload_ciphertext(self, ciphertext: bytes, key_id: str) -> str:
        response = self._client.post(
            "/api/encryption/ciphertext",
            json={"payload": list(ciphertext), "key_id": key_id},
        )
        response.raise_for_status()
        return response.json()["handle"]

    def request_prediction(self, handle: str) -> bytes:
        response = self._client.post("/api/predict", json={"ciphertext_handle": handle})
        response.raise_for_status()
        payload = response.json()["ciphertext"]
        if not isinstance(payload, list):
            raise TypeError("predict response payload must be a list of integers")

        ciphertext = bytes(int(value) for value in payload)
        logger.info("Received encrypted prediction result of %s bytes", len(ciphertext))
        return ciphertext

    def request_medical_risk_score(
        self,
        *,
        age_ciphertext: bytes,
        glucose_ciphertext: bytes,
        blood_pressure_ciphertext: bytes,
        bmi_ciphertext: bytes,
        insulin_ciphertext: bytes,
    ) -> bytes:
        response = self._client.post(
            "/api/medical/score",
            json={
                "age_ciphertext": list(age_ciphertext),
                "glucose_ciphertext": list(glucose_ciphertext),
                "blood_pressure_ciphertext": list(blood_pressure_ciphertext),
                "bmi_ciphertext": list(bmi_ciphertext),
                "insulin_ciphertext": list(insulin_ciphertext),
            },
        )
        response.raise_for_status()
        payload = response.json()["risk_score_ciphertext"]
        if not isinstance(payload, list):
            raise TypeError("medical score response payload must be a list of integers")

        ciphertext = bytes(int(value) for value in payload)
        logger.info("Received encrypted medical risk score result of %s bytes", len(ciphertext))
        return ciphertext
