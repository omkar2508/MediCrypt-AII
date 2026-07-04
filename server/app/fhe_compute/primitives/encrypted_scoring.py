from __future__ import annotations

import logging

from app.fhe_compute.primitives.encrypted_add import encrypted_add
from app.fhe_compute.primitives.encrypted_compare import encrypted_compare
from app.fhe_compute.primitives.encrypted_multiply import encrypted_multiply


logger = logging.getLogger(__name__)


def encrypted_score(values: list[bytes]) -> bytes:
    if not isinstance(values, list):
        raise TypeError("values must be a list of bytes-like objects")
    if not values:
        logger.debug("Running encrypted score over empty input")
        return b"score:empty"

    if not isinstance(values[0], (bytes, bytearray)):
        raise TypeError("values must contain bytes-like objects")

    aggregate = bytes(values[0])
    logger.debug("Running encrypted score over %s values", len(values))
    for value in values[1:]:
        if not isinstance(value, (bytes, bytearray)):
            raise TypeError("values must contain bytes-like objects")
        aggregate = encrypted_add(aggregate, value)
    return encrypted_compare(aggregate, encrypted_multiply(aggregate, bytes(values[0])))
