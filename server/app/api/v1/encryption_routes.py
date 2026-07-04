import logging

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_encryption_service, get_current_user
from app.schemas.encryption_schemas import CiphertextHandleResponse, CiphertextUploadRequest
from app.services.encryption_service import EncryptionService

router = APIRouter(prefix="/encryption", tags=["encryption"])
logger = logging.getLogger(__name__)


@router.post("/register-key", response_model=CiphertextHandleResponse)
def register_public_key(
    payload: CiphertextUploadRequest,
    current_user: str = Depends(get_current_user),
    encryption_service: EncryptionService = Depends(get_encryption_service),
) -> CiphertextHandleResponse:
    try:
        return encryption_service.register_public_key(payload, owner_id=current_user)
    except ValueError as exc:
        logger.warning("Invalid key registration request: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/ciphertext", response_model=CiphertextHandleResponse)
def upload_ciphertext(payload: CiphertextUploadRequest, encryption_service: EncryptionService = Depends(get_encryption_service)) -> CiphertextHandleResponse:
    try:
        return encryption_service.store_ciphertext(payload)
    except (TypeError, ValueError) as exc:
        logger.warning("Invalid ciphertext upload request: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/keys", response_model=list[dict])
def list_registered_keys(current_user: str = Depends(get_current_user), encryption_service: EncryptionService = Depends(get_encryption_service)):
    try:
        return encryption_service.list_public_keys(current_user)
    except Exception as exc:
        logger.exception("Failed to list registered keys: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to list registered keys") from exc
