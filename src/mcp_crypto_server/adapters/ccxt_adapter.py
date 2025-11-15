"""Adapter layer over ccxt to provide a stable interface to the rest of the app.

This adapter keeps the ccxt usage in one place and normalizes errors.
"""
from __future__ import annotations

from typing import Any, Iterable
import importlib

try:
    import ccxt  # type: ignore
except Exception:
    ccxt = importlib.import_module("ccxt")

from ..errors import ExchangeNotSupportedError


# Cache exchange instances to avoid slow re-initialization
_exchange_cache: dict[str, Any] = {}


def get_exchange(name: str) -> Any:
    """Return an exchange instance for the given name.

    Raises ExchangeNotSupportedError when the exchange factory isn't available.
    Uses caching to avoid slow re-initialization of exchanges.
    """
    name = name.lower()
    
    # Return cached instance if available
    if name in _exchange_cache:
        return _exchange_cache[name]
    
    if not hasattr(ccxt, name):
        raise ExchangeNotSupportedError(name)
    
    cls = getattr(ccxt, name)
    # Create instance with options to speed up initialization
    exchange = cls({
        'enableRateLimit': True,  # Prevent rate limit errors
        'options': {
            'defaultType': 'spot',  # Only load spot markets
        }
    })
    
    # Cache the instance
    _exchange_cache[name] = exchange
    return exchange


def fetch_ticker(exchange: Any, symbol: str) -> dict[str, Any]:
    return exchange.fetch_ticker(symbol)


def fetch_ohlcv(exchange: Any, symbol: str, timeframe: str, since: int | None, limit: int) -> Iterable[list[Any]]:
    return exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)


def fetch_order_book(exchange: Any, symbol: str, limit: int) -> dict[str, Any]:
    return exchange.fetch_order_book(symbol, limit=limit)


def fetch_tickers(exchange: Any) -> dict[str, Any]:
    return exchange.fetch_tickers()
