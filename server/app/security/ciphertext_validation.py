from __future__ import annotations

import hashlib
from datetime import datetime, timezone

from app.utils.exceptions import CiphertextCorruptedError


def compute_ciphertext_digest(ciphertext: bytes) -> str:
    return hashlib.sha256(ciphertext).hexdigest()


def validate_ciphertext_blob(ciphertext: bytes, expected_digest: str) -> None:
    if compute_ciphertext_digest(ciphertext) != expected_digest:
        raise CiphertextCorruptedError("ciphertext integrity validation failed")


def expiration_timestamp(days: int = 30) -> str:
    return datetime.now(timezone.utc).isoformat()
