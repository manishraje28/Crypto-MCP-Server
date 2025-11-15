from __future__ import annotations

from mcp_crypto_server.mcp_tools import get_current_price, get_ohlcv


def test_get_current_price_tool_smoke(monkeypatch):
    # We can monkeypatch CryptoDataClient.get_current_price via attribute access
    from mcp_crypto_server import mcp_tools

    class DummyPrice:
        def __init__(self) -> None:
            self.exchange = "dummy"
            self.symbol = "BTC/USDT"
            self.price = 123.0
            self.timestamp_ms = 0

    def fake_get_current_price(symbol: str, exchange_name: str | None = None):
        return DummyPrice()

    monkeypatch.setattr(
        mcp_tools._client(),  # noqa: SLF001
        "get_current_price",
        fake_get_current_price,
    )

    result = get_current_price(symbol="BTC/USDT", exchange="binance")
    assert result.price == 123.0


def test_get_ohlcv_tool_parameter_defaults(monkeypatch):
    from mcp_crypto_server import mcp_tools

    class DummySeries:
        def __init__(self) -> None:
            self.exchange = "dummy"
            self.symbol = "BTC/USDT"
            self.timeframe = "1h"
            self.points = []

    def fake_get_ohlcv(*args, **kwargs):
        return DummySeries()

    monkeypatch.setattr(
        mcp_tools._client(),  # noqa: SLF001
        "get_ohlcv",
        fake_get_ohlcv,
    )

    series = get_ohlcv(symbol="BTC/USDT")
    assert series.symbol == "BTC/USDT"
