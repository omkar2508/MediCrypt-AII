from __future__ import annotations

import hashlib
import hmac
import logging

logger = logging.getLogger(__name__)


def _derive_evaluation_key(secret_key: bytes) -> bytes:
    return hmac.new(secret_key, b"medicrypt-eval-key", digestmod=hashlib.sha256).digest()


def _expand_key(key: bytes, label: bytes, length: int) -> bytes:
    output = b""
    counter = 0
    while len(output) < length:
        output += hmac.new(key, label + counter.to_bytes(4, "big"), digestmod=hashlib.sha256).digest()
        counter += 1
    return output[:length]


def _derive_result_mask(eval_key: bytes, length: int) -> bytes:
    return _expand_key(eval_key, b"medicrypt-dev-result-mask", length)


def encrypt_payload(plaintext: int | str, public_key: bytes) -> bytes:
    if not public_key:
        raise ValueError("public_key must not be empty")

    try:
        value = int(plaintext)
    except (TypeError, ValueError) as exc:
        raise ValueError("plaintext must be an integer medical value") from exc

    plaintext_bytes = value.to_bytes(4, "big", signed=True)
    eval_key = _derive_evaluation_key(public_key)
    mask = _derive_result_mask(eval_key, len(plaintext_bytes))
    ciphertext = bytes(a ^ b for a, b in zip(plaintext_bytes, mask))
    logger.info("Encrypted medical value %s into %s bytes", value, len(ciphertext))
    return ciphertext
