from __future__ import annotations

import logging

from api_client import MedicryptApiClient
from decryptor import decrypt_result
from encryptor import encrypt_payload
from key_manager import KeyManager


logger = logging.getLogger(__name__)


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

    age = 54
    glucose = 168
    blood_pressure = 92
    bmi = 31
    insulin = 27

    key_manager = KeyManager()
    key_pair = key_manager.load_or_create_keys()
    private_key = key_pair.key_id.encode("utf-8")

    api_client = MedicryptApiClient(base_url="http://localhost:8000")
    try:
        age_ciphertext = encrypt_payload(age, private_key)
        glucose_ciphertext = encrypt_payload(glucose, private_key)
        blood_pressure_ciphertext = encrypt_payload(blood_pressure, private_key)
        bmi_ciphertext = encrypt_payload(bmi, private_key)
        insulin_ciphertext = encrypt_payload(insulin, private_key)

        encrypted_risk_score = api_client.request_medical_risk_score(
            age_ciphertext=age_ciphertext,
            glucose_ciphertext=glucose_ciphertext,
            blood_pressure_ciphertext=blood_pressure_ciphertext,
            bmi_ciphertext=bmi_ciphertext,
            insulin_ciphertext=insulin_ciphertext,
        )
        risk_score = decrypt_result(encrypted_risk_score, private_key)
    finally:
        api_client.close()

    print(risk_score)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())