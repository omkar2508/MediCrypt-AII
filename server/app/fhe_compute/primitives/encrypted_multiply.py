from __future__ import annotations

import logging


logger = logging.getLogger(__name__)


def encrypted_multiply(left: bytes, right: bytes) -> bytes:
    if not isinstance(left, (bytes, bytearray)):
        raise TypeError("left must be bytes-like")
    if not isinstance(right, (bytes, bytearray)):
        raise TypeError("right must be bytes-like")

    logger.debug("Running encrypted multiply over %s and %s bytes", len(left), len(right))
    return b"multiply:" + bytes(left) + b":" + bytes(right)
