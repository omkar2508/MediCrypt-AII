from app.schemas.auth_schemas import LoginRequest
from app.services.auth_service import AuthService


def test_issue_token() -> None:
    token_response = AuthService().issue_token(LoginRequest(username="demo", password="secret"))
    assert token_response.token_type == "bearer"
    assert token_response.access_token
