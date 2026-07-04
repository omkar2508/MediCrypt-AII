from datetime import datetime, timezone

from app.schemas.auth_schemas import LoginRequest, TokenResponse
from app.security.jwt_handler import create_access_token


class AuthService:
    def issue_token(self, payload: LoginRequest) -> TokenResponse:
        token = create_access_token(subject=payload.username)
        return TokenResponse(access_token=token, token_type="bearer", issued_at=datetime.now(timezone.utc))

    def validate_token(self, token: str) -> bool:
        return bool(token)
