# MCP Crypto Server

Python-based MCP server providing real-time cryptocurrency market data from major exchanges.

## Features

**REST API Endpoints:**
- `/price` - Current trading price
- `/ticker` - Bid/Ask/Last prices
- `/ohlcv` - Historical candlestick data
- `/orderbook` - Market depth (bids/asks)
- `/top_markets` - Top trading pairs

**Technology Stack:**
- FastAPI for REST endpoints
- CCXT for exchange integration
- Thread-safe TTL caching
- Pydantic data validation

## Project Structure

```
src/mcp_crypto_server/
  api/
    app.py              # FastAPI REST endpoints
  adapters/
    ccxt_adapter.py     # Exchange integration
  config.py             # Configuration
  errors.py             # Error handling
  cache.py              # TTL cache
  models.py             # Data models
  crypto_client.py      # Main client
tests/                  # Unit tests


## Quick start

This repository uses a `src/` layout. Recommended quick steps (Windows PowerShell):

1. Create and activate a virtualenv:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies (choose one):

- With pip from `requirements.txt`:

```

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Running the Server

```bash
# Navigate to src directory
cd src

# Start the server
python -m uvicorn mcp_crypto_server.api.app:app --host 127.0.0.1 --port 8000
```

Server will be available at: `http://127.0.0.1:8000`

## API Usage

**Get Bitcoin Price:**
```
GET http://127.0.0.1:8000/price?symbol=BTC/USDT&exchange=binance
```

**Get Ticker Data:**
```
GET http://127.0.0.1:8000/ticker?symbol=ETH/USDT&exchange=binance
```

**Get Historical Data:**
```
GET http://127.0.0.1:8000/ohlcv?symbol=BTC/USDT&timeframe=1h&limit=10&exchange=binance
```

**Get Order Book:**
```
GET http://127.0.0.1:8000/orderbook?symbol=BTC/USDT&depth=5&exchange=binance
```

**Get Top Markets:**
```
GET http://127.0.0.1:8000/top_markets?exchange=binance&quote_asset=USDT&limit=5
```

## Testing

```bash
pytest -q
```

## Requirements

- Python 3.10+
- FastAPI
- CCXT (real exchange data)
- Uvicorn
- Pydantic

