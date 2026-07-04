from __future__ import annotations

import time
from collections import defaultdict

from fastapi import HTTPException, Request


class SlidingWindowRateLimiter:
    def __init__(self, limit: int = 100, window_seconds: int = 60, burst: int = 200):
        self.limit = limit
        self.window_seconds = window_seconds
        self.burst = burst
        self._requests: dict[str, list[float]] = defaultdict(list)

    def allow(self, key: str) -> bool:
        now = time.monotonic()
        entries = [timestamp for timestamp in self._requests[key] if now - timestamp < self.window_seconds]
        if len(entries) >= self.burst:
            return False
        entries.append(now)
        self._requests[key] = entries
        return len(entries) <= self.limit

    async def __call__(self, request: Request, call_next):
        key = request.state.token_payload.get("sub") if hasattr(request.state, "token_payload") else request.client.host
        if not self.allow(str(key)):
            raise HTTPException(status_code=429, detail="rate_limit_exceeded")
        return await call_next(request)
