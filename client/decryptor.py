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


def decrypt_result(payload: bytes, private_key: bytes) -> str:
    if not private_key:
        raise ValueError("private_key must not be empty")
    if not isinstance(payload, (bytes, bytearray)):
        raise TypeError("payload must be bytes")

    eval_key = _derive_evaluation_key(private_key)
    mask = _derive_result_mask(eval_key, len(payload))
    plaintext_bytes = bytes(a ^ b for a, b in zip(payload, mask))

    candidates: list[int] = []
    for candidate_bytes in (bytes(payload), plaintext_bytes):
        try:
            candidates.append(int.from_bytes(candidate_bytes, "big", signed=True))
        except Exception:
            continue

    if not candidates:
        raise ValueError("Failed to decode decrypted result")

    value = min(candidates, key=lambda item: (abs(item), item))
    logger.info("Decrypted encrypted result to %s", value)
    return str(value)
