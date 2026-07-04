from __future__ import annotations

import time
from fastapi import Request
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter("medicrypt_requests_total", "Total HTTP requests", ["method", "endpoint", "http_status"])
REQUEST_LATENCY = Histogram("medicrypt_request_latency_seconds", "HTTP request latency", ["method", "endpoint"])


async def metrics_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    latency = time.time() - start
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path, http_status=str(response.status_code)).inc()
    REQUEST_LATENCY.labels(method=request.method, endpoint=request.url.path).observe(latency)
    return response
