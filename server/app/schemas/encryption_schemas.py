from pydantic import BaseModel


class CiphertextUploadRequest(BaseModel):
    handle: str | None = None
    payload: list[int]
    key_id: str


class CiphertextHandleResponse(BaseModel):
    handle: str
    status: str


class PublicKeyResponse(BaseModel):
    key_id: str
    version: str
    revoked: bool
    created_at: str


class PublicKeyListResponse(BaseModel):
    keys: list[PublicKeyResponse]
