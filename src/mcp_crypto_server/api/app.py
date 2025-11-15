"""FastAPI HTTP API exposing crypto data endpoints backed by CryptoDataClient.

Simple, synchronous endpoints for the assignment MVP.
"""
from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional

from ..config import settings
from ..crypto_client import CryptoDataClient
from ..errors import (
    CryptoServerError,
    ExchangeNotSupportedError,
    SymbolNotSupportedError,
    RateLimitError,
    UpstreamAPIError,
)

app = FastAPI(title="mcp-crypto-server")

# singleton client for simplicity
client = CryptoDataClient()


@app.exception_handler(CryptoServerError)
def crypto_exception_handler(request, exc: CryptoServerError):
    if isinstance(exc, ExchangeNotSupportedError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})
    if isinstance(exc, SymbolNotSupportedError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})
    if isinstance(exc, RateLimitError):
        return JSONResponse(status_code=429, content={"detail": str(exc)})
    return JSONResponse(status_code=502, content={"detail": str(exc)})


@app.get("/price")
def get_price(symbol: str = Query(..., description="Trading pair, e.g. BTC/USDT"), exchange: Optional[str] = None):
    try:
        price = client.get_current_price(symbol=symbol, exchange_name=exchange)
        return price.dict()
    except CryptoServerError as exc:
        raise exc


@app.get("/ticker")
def get_ticker(symbol: str = Query(...), exchange: Optional[str] = None):
    try:
        ticker = client.get_ticker(symbol=symbol, exchange_name=exchange)
        return ticker.dict()
    except CryptoServerError as exc:
        raise exc


@app.get("/ohlcv")
def get_ohlcv(
    symbol: str = Query(...),
    timeframe: str = Query("1h"),
    limit: int = Query(100, ge=1, le=1000),
    exchange: Optional[str] = None,
    since_ms: Optional[int] = None,
):
    try:
        series = client.get_ohlcv(symbol=symbol, timeframe=timeframe, limit=limit, exchange_name=exchange, since_ms=since_ms)
        return series.dict()
    except CryptoServerError as exc:
        raise exc


@app.get("/orderbook")
def get_order_book(symbol: str = Query(...), depth: int = Query(20, ge=1, le=200), exchange: Optional[str] = None):
    try:
        ob = client.get_order_book(symbol=symbol, depth=depth, exchange_name=exchange)
        return ob.dict()
    except CryptoServerError as exc:
        raise exc


@app.get("/top_markets")
def get_top_markets(exchange: Optional[str] = None, quote_asset: str = Query("USDT"), limit: int = Query(10, ge=1, le=100)):
    try:
        resp = client.get_top_markets(exchange_name=exchange, limit=limit, quote_asset=quote_asset)
        return resp.dict()
    except CryptoServerError as exc:
        raise exc
