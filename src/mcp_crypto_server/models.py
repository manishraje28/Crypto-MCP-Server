from __future__ import annotations
from typing import List, Literal
from pydantic import BaseModel, Field

class Price(BaseModel):
    exchange: str
    symbol: str
    price: float
    timestamp_ms: int


class OHLCVPoint(BaseModel):
    timestamp_ms: int = Field(..., description="Unix ms timestamp")
    open: float
    high: float
    low: float
    close: float
    volume: float


class OHLCVSeries(BaseModel):
    exchange: str
    symbol: str
    timeframe: str
    points: List[OHLCVPoint]


class OrderBookLevel(BaseModel):
    price: float
    amount: float


class OrderBook(BaseModel):
    exchange: str
    symbol: str
    bids: list[OrderBookLevel]
    asks: list[OrderBookLevel]


class TopMarket(BaseModel):
    symbol: str
    price: float
    quote_asset: str
    base_asset: str | None = None


class TopMarketsResponse(BaseModel):
    exchange: str
    markets: list[TopMarket]


# For "real-time" ticks
class Ticker(BaseModel):
    exchange: str
    symbol: str
    bid: float | None
    ask: float | None
    last: float | None
    timestamp_ms: int | None
    info_source: Literal["ccxt"]
