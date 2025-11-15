from __future__ import annotations
import time

from mcp_crypto_server.cache import TTLCache


def test_cache_sets_and_gets():
    cache = TTLCache(ttl_seconds=5)
    cache.set(("k", 1), "value")
    assert cache.get(("k", 1)) == "value"


def test_cache_expires():
    cache = TTLCache(ttl_seconds=1)
    cache.set("key", "value")
    time.sleep(1.2)
    assert cache.get("key") is None
