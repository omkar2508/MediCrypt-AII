from __future__ import annotations

from fastapi import Request
from starlette.responses import Response


async def security_middleware(request: Request, call_next):
    response: Response = await call_next(request)

    response.headers.setdefault(
        "Strict-Transport-Security",
        "max-age=63072000; includeSubDomains; preload"
    )

    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "no-referrer")
    response.headers.setdefault(
        "Permissions-Policy",
        "geolocation=(), microphone=()"
    )

    # Allow Swagger UI resources while keeping CSP reasonably secure
    response.headers.setdefault(
        "Content-Security-Policy",
        (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https://fastapi.tiangolo.com; "
            "font-src 'self' https://cdn.jsdelivr.net; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "object-src 'none';"
        ),
    )

    response.headers.setdefault(
        "Cross-Origin-Embedder-Policy",
        "require-corp"
    )

    response.headers.setdefault(
        "Cross-Origin-Opener-Policy",
        "same-origin"
    )

    response.headers.setdefault(
        "Cross-Origin-Resource-Policy",
        "same-origin"
    )

    return response