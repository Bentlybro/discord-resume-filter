import time


class MoveTracker:
    def __init__(self, max_moves: int = 1, window_seconds: int = 300):
        self._max = max_moves
        self._window = window_seconds
        self._events: dict[int, list[float]] = {}

    def can_move(self, user_id: int) -> bool:
        return self._count_recent(user_id) < self._max

    def record(self, user_id: int) -> None:
        now = time.monotonic()
        history = self._events.setdefault(user_id, [])
        history.append(now)
        self._purge(history, now)

    def _count_recent(self, user_id: int) -> int:
        history = self._events.get(user_id)
        if not history:
            return 0
        now = time.monotonic()
        self._purge(history, now)
        return len(history)

    def _purge(self, history: list[float], now: float) -> None:
        cutoff = now - self._window
        history[:] = [t for t in history if t > cutoff]
