from __future__ import annotations

from typing import Annotated
import time
import base64
import importlib
from typing import Callable

try:
    from pydantic import Field
except Exception:  # pragma: no cover - optional dependency
    # minimal Field shim for type annotations if pydantic not installed
    def Field(*_args, **_kwargs):
        return None

# Try to import real MCP machinery; otherwise provide a tiny local shim so
# the module can be imported in environments that don't have `mcp` installed.
try:
    mcp_module = importlib.import_module("mcp.server.fastmcp")
    FastMCP = getattr(mcp_module, "FastMCP")
except Exception:  # pragma: no cover - fallback shim
    class _Tool:
        def __init__(self, func: Callable):
            self.func = func

        def __call__(self, *args, **kwargs):
            return self.func(*args, **kwargs)

    class FastMCP:
        def __init__(self, name: str = "fastmcp-shim") -> None:
            self.name = name
            self._tools = {}

        def tool(self, *args, **kwargs):
            def _decorator(fn: Callable):
                # store metadata, but return function untouched
                self._tools[fn.__name__] = fn
                return fn

            return _decorator


from mcp_crypto_server.crypto_client import CryptoDataClient
from mcp_crypto_server.errors import *
from mcp_crypto_server.models import *

# App context for dependency injection
class AppContext:
    def __init__(self) -> None:
        self.client = CryptoDataClient()


mcp = FastMCP(name="Crypto Market MCP Server")

# We keep a single AppContext here for simplicity
app_context = AppContext()


def _client() -> CryptoDataClient:
    return app_context.client


@mcp.tool()
def get_current_price(
    symbol: Annotated[str, Field(description="Trading pair, e.g. BTC/USDT")],
    exchange: Annotated[str | None, Field(description="Exchange id, e.g. binance")] = None,
) -> Price:
    try:
        return _client().get_current_price(symbol=symbol, exchange_name=exchange)
    except CryptoServerError as exc:
        raise RuntimeError(user_friendly_message(exc)) from exc


@mcp.tool()
def get_ticker(
    symbol: Annotated[str, Field(description="Trading pair, e.g. BTC/USDT")],
    exchange: Annotated[str | None, Field(description="Exchange id, e.g. binance")] = None,
) -> Ticker:
    try:
        return _client().get_ticker(symbol=symbol, exchange_name=exchange)
    except CryptoServerError as exc:
        raise RuntimeError(user_friendly_message(exc)) from exc


@mcp.tool()
def get_ohlcv(
    symbol: Annotated[str, Field(description="Trading pair, e.g. BTC/USDT")],
    timeframe: Annotated[str, Field(description="Timeframe, e.g. 1m, 5m, 1h, 1d")] = "1h",
    limit: Annotated[int, Field(ge=1, le=1000)] = 100,
    exchange: Annotated[str | None, Field(description="Exchange id, e.g. binance")] = None,
    since_ms: Annotated[int | None, Field(description="Unix timestamp in ms")] = None,
) -> OHLCVSeries:
    try:
        return _client().get_ohlcv(
            symbol=symbol,
            timeframe=timeframe,
            limit=limit,
            exchange_name=exchange,
            since_ms=since_ms,
        )
    except CryptoServerError as exc:
        raise RuntimeError(user_friendly_message(exc)) from exc


@mcp.tool()
def get_order_book(
    symbol: Annotated[str, Field(description="Trading pair, e.g. BTC/USDT")],
    depth: Annotated[int, Field(ge=1, le=100)] = 20,
    exchange: Annotated[str | None, Field(description="Exchange id, e.g. binance")] = None,
) -> OrderBook:
    try:
        return _client().get_order_book(
            symbol=symbol,
            depth=depth,
            exchange_name=exchange,
        )
    except CryptoServerError as exc:
        raise RuntimeError(user_friendly_message(exc)) from exc


@mcp.tool()
def get_top_markets(
    exchange: Annotated[str | None, Field(description="Exchange id, e.g. binance")] = None,
    quote_asset: Annotated[str, Field(description="Quote asset to filter by, e.g. USDT")] = "USDT",
    limit: Annotated[int, Field(ge=1, le=50)] = 10,
) -> TopMarketsResponse:
    try:
        return _client().get_top_markets(
            exchange_name=exchange,
            limit=limit,
            quote_asset=quote_asset,
        )
    except CryptoServerError as exc:
        raise RuntimeError(user_friendly_message(exc)) from exc


# Backwards-compatible base64 helpers (previous API in this repo)
def b64_encode(data: bytes) -> str:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes")
    return base64.b64encode(data).decode("ascii")


def b64_decode(s: str) -> bytes:
    if not isinstance(s, str):
        raise TypeError("s must be str")
    return base64.b64decode(s.encode("ascii"))
