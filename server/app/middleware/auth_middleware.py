from fastapi import Request

from app.security.jwt_handler import decode_access_token


async def auth_middleware(request: Request, call_next):
    authorization = request.headers.get("Authorization")
    if authorization and authorization.startswith("Bearer "):
        token = authorization.removeprefix("Bearer ").strip()
        request.state.token_payload = decode_access_token(token)
    return await call_next(request)
