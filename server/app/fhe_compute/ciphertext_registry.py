from __future__ import annotations

import logging


logger = logging.getLogger(__name__)


class CiphertextRegistry:
    def __init__(self) -> None:
        self._store: dict[str, tuple[bytes, str]] = {}

    def put(self, handle: str, blob: bytes, key_id: str) -> None:
        if not isinstance(handle, str) or not handle.strip():
            raise ValueError("handle must be a non-empty string")
        if not isinstance(key_id, str) or not key_id.strip():
            raise ValueError("key_id must be a non-empty string")
        if not isinstance(blob, (bytes, bytearray)):
            raise TypeError("blob must be bytes-like")

        logger.info("Storing ciphertext handle %s with %s bytes for key %s", handle, len(blob), key_id)
        self._store[handle] = (bytes(blob), key_id)

    def get(self, handle: str) -> bytes:
        if not isinstance(handle, str) or not handle.strip():
            raise ValueError("handle must be a non-empty string")

        entry = self._store.get(handle)
        if entry is None:
            logger.warning("Ciphertext handle %s not found", handle)
            raise KeyError(f"Ciphertext handle not found: {handle}")

        blob, _ = entry
        logger.debug("Loaded ciphertext handle %s with %s bytes", handle, len(blob))
        return blob

    def get_key_id(self, handle: str) -> str:
        if not isinstance(handle, str) or not handle.strip():
            raise ValueError("handle must be a non-empty string")

        entry = self._store.get(handle)
        if entry is None:
            logger.warning("Ciphertext handle %s not found", handle)
            raise KeyError(f"Ciphertext handle not found: {handle}")

        _, key_id = entry
        logger.debug("Loaded key_id %s for ciphertext handle %s", key_id, handle)
        return key_id
