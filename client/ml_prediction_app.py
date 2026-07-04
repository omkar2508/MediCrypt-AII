from __future__ import annotations

import logging

from api_client import MedicryptApiClient
from decryptor import decrypt_result
from encryptor import encrypt_payload
from key_manager import KeyManager

logger = logging.getLogger(__name__)


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

    age = 50
    glucose = 160
    blood_pressure = 90
    bmi = 30
    insulin = 20

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

        encrypted_prediction = api_client.request_prediction(handle=api_client.upload_ciphertext(age_ciphertext, key_pair.key_id))
        prediction = decrypt_result(encrypted_prediction, private_key)

        print("Encrypted diabetes prediction result:", prediction)
        return 0
    finally:
        api_client.close()


if __name__ == "__main__":
    raise SystemExit(main())
