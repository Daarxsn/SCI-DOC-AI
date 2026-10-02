from collections import defaultdict
from time import monotonic


class InMemoryRateLimiter:
    """Development limiter; production should use a shared gateway/Redis limiter."""

    def __init__(self, limit: int = 60, window_seconds: int = 60):
        self.limit = limit
        self.window_seconds = window_seconds
        self._events = defaultdict(list)

    def allow(self, key: str) -> bool:
        now = monotonic()
        events = [t for t in self._events[key] if now - t < self.window_seconds]
        if len(events) >= self.limit:
            self._events[key] = events
            return False
        events.append(now)
        self._events[key] = events
        return True
