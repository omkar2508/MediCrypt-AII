from __future__ import annotations

import logging
import sys

from api_client import MedicryptApiClient
from decryptor import decrypt_result
from encryptor import encrypt_payload
from key_manager import KeyManager


logger = logging.getLogger(__name__)


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

    try:
        key_manager = KeyManager()
        key_pair = key_manager.load_or_create_keys()
        private_key = key_pair.key_id.encode("utf-8")

        api_client = MedicryptApiClient(base_url="http://localhost:8000")
        try:
            ciphertext = encrypt_payload(42, private_key)
            handle = api_client.upload_ciphertext(ciphertext=ciphertext, key_id=key_pair.key_id)
            encrypted_result = api_client.request_prediction(handle=handle)
            result = decrypt_result(encrypted_result, private_key)
        finally:
            api_client.close()

        print(result)
        return 0
    except Exception:
        logger.exception("Client workflow failed")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
