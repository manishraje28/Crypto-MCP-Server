from __future__ import annotations
from typing import Any

import types
import ccxt  # type: ignore
import pytest

from mcp_crypto_server.crypto_client import CryptoDataClient
from mcp_crypto_server.errors import SymbolNotSupportedError


class DummyExchange:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.fetch_ticker_called = False
        self.fetch_ohlcv_called = False

    def fetch_ticker(self, symbol: str) -> dict[str, Any]:
        self.fetch_ticker_called = True
        if symbol != "BTC/USDT":
            raise ccxt.BadSymbol("Bad symbol")
        return {
            "symbol": symbol,
            "last": 50000.0,
            "timestamp": 1700000000000,
        }

    def fetch_ohlcv(self, symbol: str, timeframe: str, since: int | None, limit: int):
        self.fetch_ohlcv_called = True
        return [
            [1700000000000, 49000, 51000, 48000, 50000, 123.45],
        ]


@pytest.fixture(autouse=True)
def patch_ccxt_binance(monkeypatch: pytest.MonkeyPatch) -> None:
    # Replace ccxt.binance with DummyExchange factory
    monkeypatch.setattr(ccxt, "binance", DummyExchange)


def test_get_current_price_success():
    client = CryptoDataClient()
    price = client.get_current_price("BTC/USDT", exchange_name="binance")
    assert price.symbol == "BTC/USDT"
    assert price.price == 50000.0


def test_get_current_price_bad_symbol():
    client = CryptoDataClient()
    with pytest.raises(SymbolNotSupportedError):
        client.get_current_price("XXX/YYY", exchange_name="binance")


def test_get_ohlcv_success():
    client = CryptoDataClient()
    series = client.get_ohlcv("BTC/USDT", timeframe="1h", limit=1, exchange_name="binance")
    assert series.symbol == "BTC/USDT"
    assert len(series.points) == 1
    point = series.points[0]
    assert point.close == 50000.0
