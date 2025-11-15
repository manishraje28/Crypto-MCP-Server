from __future__ import annotations
import os
from dataclasses import dataclass

@dataclass
class Settings:
    """
    Application settings.

    In a real deployment you might pass API keys here
    (e.g. CoinMarketCap) via environment variables.
    """
    default_exchange: str = os.getenv("DEFAULT_EXCHANGE", "binance")
    cache_ttl_seconds: int = int(os.getenv("CACHE_TTL_SECONDS", "10"))
    # if you later add CoinMarketCap:
    coinmarketcap_api_key: str | None = os.getenv("COINMARKETCAP_API_KEY")

settings = Settings()
