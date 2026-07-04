from __future__ import annotations

import logging


logger = logging.getLogger(__name__)


def serialize_ciphertext(blob: bytes) -> list[int]:
    if not isinstance(blob, (bytes, bytearray)):
        raise TypeError("blob must be bytes-like")

    logger.debug("Serializing ciphertext payload with %s bytes", len(blob))
    return list(blob)


def deserialize_ciphertext(payload: list[int]) -> bytes:
    if not isinstance(payload, list):
        raise TypeError("payload must be a list of integers")

    try:
        blob = bytes(int(value) for value in payload)
    except (TypeError, ValueError) as exc:
        raise ValueError("payload must contain only integer byte values") from exc

    logger.debug("Deserialized ciphertext payload with %s bytes", len(blob))
    return blob
