from __future__ import annotations

import logging
from uuid import uuid4

from app.fhe_compute.ciphertext_registry import CiphertextRegistry
from app.fhe_compute.serialization import deserialize_ciphertext
from app.schemas.encryption_schemas import CiphertextHandleResponse, CiphertextUploadRequest
from sqlalchemy.orm import Session
import base64
from sqlalchemy.exc import IntegrityError
from app.models.public_evaluation_key import PublicEvaluationKey


logger = logging.getLogger(__name__)


_REGISTRY = CiphertextRegistry()


class EncryptionService:
    def __init__(self, db: Session):
        self.db = db

    def register_public_key(self, payload: CiphertextUploadRequest, owner_id: str) -> CiphertextHandleResponse:
        if not payload.key_id or not payload.key_id.strip():
            raise ValueError("key_id must not be empty")
        if not payload.payload:
            raise ValueError("payload must not be empty for key registration")

        try:
            # store the key material as base64
            key_bytes = bytes(payload.payload)
            key_b64 = base64.b64encode(key_bytes).decode('ascii')
            key = PublicEvaluationKey(owner_id=owner_id, key_id=payload.key_id, key_material=key_b64)
            self.db.add(key)
            self.db.commit()
            self.db.refresh(key)
            logger.info("Registered public evaluation key %s for owner %s", payload.key_id, owner_id)
            return CiphertextHandleResponse(handle=key.key_id, status="registered")
        except IntegrityError:
            self.db.rollback()
            raise ValueError("A key with this key_id already exists")

    def list_public_keys(self, owner_id: str) -> list[dict]:
        # Return a list of dicts with key_id, version, revoked, created_at
        rows = (
            self.db.query(PublicEvaluationKey)
            .filter(PublicEvaluationKey.owner_id == owner_id)
            .order_by(PublicEvaluationKey.created_at.desc())
            .all()
        )
        result = []
        for r in rows:
            result.append({
                "key_id": r.key_id,
                "version": r.version,
                "revoked": bool(r.revoked),
                "created_at": r.created_at.isoformat() if r.created_at else None,
            })
        return result

    def store_ciphertext(self, payload: CiphertextUploadRequest) -> CiphertextHandleResponse:
        if not payload.key_id.strip():
            raise ValueError("key_id must not be empty")

        handle = payload.handle or str(uuid4())
        ciphertext = deserialize_ciphertext(payload.payload)
        _REGISTRY.put(handle, ciphertext, payload.key_id)
        logger.info("Stored ciphertext for handle %s under key %s", handle, payload.key_id)
        return CiphertextHandleResponse(handle=handle, status="stored")

    def get_ciphertext_key_id(self, handle: str) -> str:
        return _REGISTRY.get_key_id(handle)

    def load_ciphertext(self, handle: str) -> bytes:
        blob = _REGISTRY.get(handle)
        logger.debug("Loaded ciphertext payload for handle %s", handle)
        return blob
