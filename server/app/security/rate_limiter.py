from collections import defaultdict
from time import monotonic


class RateLimiter:
    def __init__(self, limit: int = 100, window_seconds: int = 60) -> None:
        self.limit = limit
        self.window_seconds = window_seconds
        self._requests: dict[str, list[float]] = defaultdict(list)

    def allow(self, key: str) -> bool:
        now = monotonic()
        entries = [timestamp for timestamp in self._requests[key] if now - timestamp < self.window_seconds]
        entries.append(now)
        self._requests[key] = entries
        return len(entries) <= self.limit
