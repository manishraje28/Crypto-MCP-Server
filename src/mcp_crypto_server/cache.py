from __future__ import annotations
import time
from dataclasses import dataclass
from typing import Any, Hashable
import threading

@dataclass
class CacheEntry:
    value: Any
    expires_at: float

class TTLCache:
    """
    Very simple in-memory TTL cache.
    Designed for read-heavy, low-volume MCP tool calls.
    """

    def __init__(self, ttl_seconds: int = 10) -> None:
        self._ttl = ttl_seconds
        self._store: dict[Hashable, CacheEntry] = {}
        self._lock = threading.Lock()

    def _now(self) -> float:
        return time.time()

    def get(self, key: Hashable) -> Any | None:
        with self._lock:
            entry = self._store.get(key)
            if not entry:
                return None
            if entry.expires_at < self._now():
                # expired
                self._store.pop(key, None)
                return None
            return entry.value

    def set(self, key: Hashable, value: Any) -> None:
        with self._lock:
            self._store[key] = CacheEntry(value=value, expires_at=self._now() + self._ttl)

    def clear(self) -> None:
        with self._lock:
            self._store.clear()
