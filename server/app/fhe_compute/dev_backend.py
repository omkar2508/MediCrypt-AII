from __future__ import annotations

import hashlib
import hmac
from typing import Any

from app.fhe_compute.engine_interface import EncryptedComputeEngine


def _hmac(key: bytes, message: bytes) -> bytes:
    return hmac.new(key, message, hashlib.sha256).digest()


def _xor_bytes(data: bytes, mask: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(data, mask))


def _expand_key(key: bytes, label: bytes, length: int) -> bytes:
    output = b""
    counter = 0
    while len(output) < length:
        output += _hmac(key, label + counter.to_bytes(4, "big"))
        counter += 1
    return output[:length]


def derive_evaluation_key(secret_key: bytes) -> bytes:
    return _hmac(secret_key, b"medicrypt-eval-key")


def derive_cipher_mask(secret_key: bytes, length: int) -> bytes:
    return _expand_key(secret_key, b"medicrypt-ct-mask", length)


def derive_result_mask(eval_key: bytes, length: int) -> bytes:
    return _expand_key(eval_key, b"medicrypt-dev-result-mask", length)


class DevPythonEngine(EncryptedComputeEngine):
    def add(self, left: bytes, right: bytes) -> bytes:
        return b"dev-add:" + left + b":" + right

    def multiply(self, left: bytes, right: bytes) -> bytes:
        return b"dev-mul:" + left + b":" + right

    def compare(self, left: bytes, right: bytes) -> bytes:
        return b"dev-cmp:" + left + b":" + right

    def score(self, values: list[bytes]) -> bytes:
        return b"dev-scr:" + b"|".join(values)

    def evaluate_prediction(self, ciphertext: bytes, key_material: bytes | None = None) -> bytes:
        if not key_material:
            raise ValueError("evaluation key material is required for dev prediction")
        mask = derive_result_mask(key_material, len(ciphertext))
        return _xor_bytes(ciphertext, mask)

    def decrypt_prediction(self, encrypted_prediction: bytes, key_material: bytes) -> int:
        masked = _xor_bytes(encrypted_prediction, derive_result_mask(key_material, len(encrypted_prediction)))
        value = int.from_bytes(masked[:4], "big", signed=False)
        return value
