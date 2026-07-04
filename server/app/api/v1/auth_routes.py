from fastapi import APIRouter, Depends

from app.api.deps import get_auth_service
from app.schemas.auth_schemas import LoginRequest, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=TokenResponse)
def issue_token(payload: LoginRequest, auth_service: AuthService = Depends(get_auth_service)) -> TokenResponse:
    return auth_service.issue_token(payload)
