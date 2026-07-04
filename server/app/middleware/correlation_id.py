from __future__ import annotations

import uuid

from fastapi import Request


async def correlation_id_middleware(request: Request, call_next):
    correlation_id = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
    request.state.correlation_id = correlation_id
    response = await call_next(request)
    response.headers.setdefault("X-Correlation-ID", correlation_id)
    return response
