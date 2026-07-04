from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CiphertextEnvelope:
    handle: str
    key_id: str
    ciphertext: bytes
