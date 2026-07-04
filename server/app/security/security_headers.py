from fastapi import FastAPI


def add_security_headers(app: FastAPI) -> None:
    @app.middleware("http")
    async def security_headers_middleware(request, call_next):
        response = await call_next(request)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        return response
