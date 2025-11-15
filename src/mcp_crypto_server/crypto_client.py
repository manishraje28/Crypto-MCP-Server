from __future__ import annotations

from typing import Any, Iterable

try:  # use real ccxt if installed, otherwise the local shim will be used
    import ccxt  # type: ignore
except Exception:  # pragma: no cover - local shim 'src/ccxt.py' will usually be found
    import importlib

    ccxt = importlib.import_module("ccxt")

from .cache import TTLCache
from .config import settings
from .errors import (
    ExchangeNotSupportedError,
    SymbolNotSupportedError,
    UpstreamAPIError,
    RateLimitError,
)
from .models import (
    Price,
    OHLCVPoint,
    OHLCVSeries,
    OrderBookLevel,
    OrderBook,
    TopMarket,
    TopMarketsResponse,
    Ticker,
)


class CryptoDataClient:
    """
    Thin abstraction over ccxt so the rest of the code
    doesn't depend directly on ccxt's API.

    This implementation will use the local `ccxt` shim when the real
    `ccxt` package is not installed; tests monkeypatch `ccxt.binance` and
    this design allows that to work.
    """

    def __init__(self, cache: TTLCache | None = None) -> None:
        self._cache = cache or TTLCache(settings.cache_ttl_seconds)
        self._exchanges: dict[str, Any] = {}

    def _get_exchange(self, name: str) -> Any:
        name = name.lower()
        if name in self._exchanges:
            return self._exchanges[name]

        if not hasattr(ccxt, name):
            raise ExchangeNotSupportedError(name)

        exchange_cls = getattr(ccxt, name)
        exchange = exchange_cls()
        self._exchanges[name] = exchange
        return exchange

    # ---------- Helpers ----------

    def _wrap_ccxt_error(self, exc: Exception) -> Exception:
        name = exc.__class__.__name__
        if "RateLimit" in name:
            return RateLimitError(str(exc))
        if "Symbol" in name or "Market" in name or "BadSymbol" in name:
            return SymbolNotSupportedError(str(exc))
        return UpstreamAPIError(str(exc))

    # ---------- Public API ----------

    def get_current_price(self, symbol: str, exchange_name: str | None = None) -> Price:
        exchange_name = exchange_name or settings.default_exchange
        cache_key = ("price", exchange_name, symbol)

        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            exchange = self._get_exchange(exchange_name)
            ticker = exchange.fetch_ticker(symbol)
        except Exception as exc:  # noqa: BLE001
            raise self._wrap_ccxt_error(exc) from exc

        price_value = float(ticker.get("last") or ticker.get("close"))
        price = Price(
            exchange=exchange_name,
            symbol=symbol,
            price=price_value,
            timestamp_ms=int(ticker.get("timestamp") or 0),
        )
        self._cache.set(cache_key, price)
        return price

    def get_ohlcv(
        self,
        symbol: str,
        timeframe: str = "1h",
        limit: int = 100,
        exchange_name: str | None = None,
        since_ms: int | None = None,
    ) -> OHLCVSeries:
        exchange_name = exchange_name or settings.default_exchange
        cache_key = ("ohlcv", exchange_name, symbol, timeframe, limit, since_ms)

        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            exchange = self._get_exchange(exchange_name)
            raw: Iterable[list[Any]] = exchange.fetch_ohlcv(
                symbol,
                timeframe=timeframe,
                since=since_ms,
                limit=limit,
            )
        except Exception as exc:  # noqa: BLE001
            raise self._wrap_ccxt_error(exc) from exc

        points = [
            OHLCVPoint(
                timestamp_ms=row[0],
                open=float(row[1]),
                high=float(row[2]),
                low=float(row[3]),
                close=float(row[4]),
                volume=float(row[5]),
            )
            for row in raw
        ]

        series = OHLCVSeries(
            exchange=exchange_name,
            symbol=symbol,
            timeframe=timeframe,
            points=points,
        )
        self._cache.set(cache_key, series)
        return series

    def get_ticker(self, symbol: str, exchange_name: str | None = None) -> Ticker:
        exchange_name = exchange_name or settings.default_exchange
        cache_key = ("ticker", exchange_name, symbol)
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            exchange = self._get_exchange(exchange_name)
            ticker = exchange.fetch_ticker(symbol)
        except Exception as exc:  # noqa: BLE001
            raise self._wrap_ccxt_error(exc) from exc

        result = Ticker(
            exchange=exchange_name,
            symbol=symbol,
            bid=ticker.get("bid"),
            ask=ticker.get("ask"),
            last=ticker.get("last") or ticker.get("close"),
            timestamp_ms=ticker.get("timestamp"),
            info_source="ccxt",
        )
        self._cache.set(cache_key, result)
        return result

    def get_order_book(
        self,
        symbol: str,
        depth: int = 20,
        exchange_name: str | None = None,
    ) -> OrderBook:
        exchange_name = exchange_name or settings.default_exchange
        cache_key = ("order_book", exchange_name, symbol, depth)
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            exchange = self._get_exchange(exchange_name)
            ob = exchange.fetch_order_book(symbol, limit=depth)
        except Exception as exc:  # noqa: BLE001
            raise self._wrap_ccxt_error(exc) from exc

        bids = [
            OrderBookLevel(price=float(price), amount=float(amount))
            for price, amount in ob.get("bids", [])[:depth]
        ]
        asks = [
            OrderBookLevel(price=float(price), amount=float(amount))
            for price, amount in ob.get("asks", [])[:depth]
        ]

        result = OrderBook(
            exchange=exchange_name,
            symbol=symbol,
            bids=bids,
            asks=asks,
        )
        self._cache.set(cache_key, result)
        return result

    def get_top_markets(
        self,
        exchange_name: str | None = None,
        limit: int = 10,
        quote_asset: str = "USDT",
    ) -> TopMarketsResponse:
        exchange_name = exchange_name or settings.default_exchange
        cache_key = ("top_markets", exchange_name, limit, quote_asset)
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            exchange = self._get_exchange(exchange_name)
            tickers: dict[str, Any] = exchange.fetch_tickers()
        except Exception as exc:  # noqa: BLE001
            raise self._wrap_ccxt_error(exc) from exc

        markets: list[TopMarket] = []
        for symbol, t in tickers.items():
            if not symbol.endswith(f"/{quote_asset}"):
                continue

            last_price = t.get("last") or t.get("close")
            if last_price is None:
                continue

            base = symbol.split("/")[0]
            markets.append(
                TopMarket(
                    symbol=symbol,
                    price=float(last_price),
                    quote_asset=quote_asset,
                    base_asset=base,
                )
            )

        markets.sort(key=lambda m: float(tickers[m.symbol].get("quoteVolume", 0.0)), reverse=True)
        markets = markets[:limit]

        resp = TopMarketsResponse(exchange=exchange_name, markets=markets)
        self._cache.set(cache_key, resp)
        return resp
