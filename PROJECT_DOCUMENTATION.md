# MCP Crypto Server - Project Documentation

## 📋 Project Overview

A production-ready Python-based Model Context Protocol (MCP) server that retrieves real-time and historical cryptocurrency market data from major exchanges using the CCXT library.

**Assignment Compliance:**
- ✅ Real-time cryptocurrency data fetching
- ✅ Historical market data queries
- ✅ Multiple exchange support (Binance, Coinbase, Kraken, etc.)
- ✅ Robust error handling and validation
- ✅ In-memory caching for performance
- ✅ Comprehensive test coverage
- ✅ RESTful API endpoints
- ✅ Production-ready code structure

---

## 🏗️ Architecture

### Technology Stack
- **Framework:** FastAPI (async-capable, production-ready)
- **Exchange Integration:** CCXT (unified API for 100+ exchanges)
- **Validation:** Pydantic (data models with type safety)
- **Caching:** Thread-safe TTL cache
- **Server:** Uvicorn ASGI server
- **Testing:** Pytest with comprehensive coverage

### Design Patterns
- **Adapter Pattern:** CCXT integration abstracted for flexibility
- **Repository Pattern:** CryptoDataClient as central data access layer
- **Dependency Injection:** FastAPI's native DI system
- **Error Handling:** Centralized exception handling with custom error types

---

## 🚀 Features Implemented

### Core MCP Features

#### 1. Real-Time Data Endpoints
- **GET /price** - Current trading price
  - Exchange selection
  - Multiple trading pairs
  - Real-time price updates
  
- **GET /ticker** - Complete ticker data
  - Bid/Ask/Last prices
  - 24h volume
  - Price changes
  
- **GET /orderbook** - Market depth
  - Configurable depth (1-200 levels)
  - Bids and asks with prices/amounts
  - Real-time order book snapshots

#### 2. Historical Data Endpoints
- **GET /ohlcv** - Candlestick data
  - Multiple timeframes (1m, 5m, 15m, 1h, 4h, 1d, 1w)
  - Configurable limit (1-1000 candles)
  - Since timestamp support
  - Open/High/Low/Close/Volume data

#### 3. Utility Endpoints
- **GET /top_markets** - Popular trading pairs
  - Filter by quote asset (USDT, BTC, etc.)
  - Configurable result limit
  - Price information included

### Robustness Features

#### Error Handling
```python
# Custom exception hierarchy
- CryptoServerError (base)
  - ExchangeNotSupportedError
  - SymbolNotSupportedError
  - RateLimitError
  - UpstreamAPIError
```

#### Caching System
- Thread-safe implementation
- Configurable TTL (default 10 seconds)
- Exchange instance caching (prevents slow re-initialization)
- Automatic cache cleanup

#### Data Validation
- Pydantic models for all responses
- Type safety throughout
- Input validation with FastAPI Query parameters
- Structured error responses

---

## 📁 Project Structure

```
mcp-crypto-server/
├── src/
│   └── mcp_crypto_server/
│       ├── api/
│       │   ├── app.py              # FastAPI REST endpoints
│       │   └── __init__.py
│       ├── adapters/
│       │   ├── ccxt_adapter.py     # CCXT integration layer
│       │   └── __init__.py
│       ├── cache.py                # Thread-safe TTL cache
│       ├── config.py               # Configuration management
│       ├── crypto_client.py        # Main data client
│       ├── errors.py               # Custom exceptions
│       ├── mcp_tools.py            # MCP protocol tools
│       ├── models.py               # Pydantic data models
│       ├── server.py               # MCP server entry point
│       └── __init__.py
├── tests/
│   ├── conftest.py                 # Pytest configuration
│   ├── test_cache.py               # Cache unit tests
│   ├── test_crypto_client.py      # Client integration tests
│   └── test_mcp_tools.py           # MCP tools tests
├── .env                            # Environment configuration
├── .gitignore                      # Git ignore rules
├── README.md                       # User documentation
├── requirements.txt                # Python dependencies
├── pyproject.toml                  # Project metadata
└── run_server.py                   # Server launcher
```

---

## 🧪 Test Coverage

### Test Suite Overview

#### 1. Cache Tests (`test_cache.py`)
- ✅ Basic get/set operations
- ✅ TTL expiration behavior
- ✅ Cache cleanup on expiry
- ✅ Thread safety validation
- ✅ Multiple key handling

#### 2. Client Tests (`test_crypto_client.py`)
- ✅ Current price retrieval
- ✅ Ticker data validation
- ✅ OHLCV historical data
- ✅ Order book depth queries
- ✅ Top markets listing
- ✅ Error handling for invalid inputs
- ✅ Exchange validation
- ✅ Symbol validation

#### 3. MCP Tools Tests (`test_mcp_tools.py`)
- ✅ Tool registration
- ✅ Input/output validation
- ✅ Error propagation
- ✅ MCP protocol compliance

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/mcp_crypto_server

# Run specific test file
pytest tests/test_cache.py -v

# Run with output
pytest -v -s
```

---

## 🔧 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Internet connection (for exchange API access)

### Installation Steps

1. **Clone the repository:**
```bash
git clone <repository-url>
cd mcp-crypto-server
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Start the server:**
```bash
cd src
python -m uvicorn mcp_crypto_server.api.app:app --host 127.0.0.1 --port 8000
```

4. **Verify installation:**
```bash
# Open browser
http://127.0.0.1:8000/docs

# Or test endpoint
curl "http://127.0.0.1:8000/price?symbol=BTC/USDT&exchange=binance"
```

---

## 📊 API Documentation

### Endpoint: GET /price

**Description:** Get current trading price for a symbol

**Parameters:**
- `symbol` (required): Trading pair (e.g., "BTC/USDT")
- `exchange` (optional): Exchange name (default: "binance")

**Example Request:**
```bash
GET http://127.0.0.1:8000/price?symbol=BTC/USDT&exchange=binance
```

**Example Response:**
```json
{
  "exchange": "binance",
  "symbol": "BTC/USDT",
  "price": 96254.61,
  "timestamp_ms": 1763230278013
}
```

---

### Endpoint: GET /ticker

**Description:** Get ticker data with bid/ask/last prices

**Parameters:**
- `symbol` (required): Trading pair
- `exchange` (optional): Exchange name

**Example Request:**
```bash
GET http://127.0.0.1:8000/ticker?symbol=ETH/USDT&exchange=binance
```

**Example Response:**
```json
{
  "exchange": "binance",
  "symbol": "ETH/USDT",
  "bid": 3654.2,
  "ask": 3654.25,
  "last": 3654.22,
  "timestamp_ms": 1763225099558,
  "info_source": "ccxt"
}
```

---

### Endpoint: GET /ohlcv

**Description:** Get historical candlestick (OHLCV) data

**Parameters:**
- `symbol` (required): Trading pair
- `timeframe` (optional): Candle timeframe (default: "1h")
  - Valid: 1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w
- `limit` (optional): Number of candles (default: 100, max: 1000)
- `since_ms` (optional): Start timestamp in milliseconds
- `exchange` (optional): Exchange name

**Example Request:**
```bash
GET http://127.0.0.1:8000/ohlcv?symbol=BTC/USDT&timeframe=1h&limit=10&exchange=binance
```

**Example Response:**
```json
{
  "exchange": "binance",
  "symbol": "BTC/USDT",
  "timeframe": "1h",
  "points": [
    {
      "timestamp_ms": 1731686400000,
      "open": 96000.0,
      "high": 96500.0,
      "low": 95800.0,
      "close": 96200.0,
      "volume": 1234.56
    }
  ]
}
```

---

### Endpoint: GET /orderbook

**Description:** Get order book (market depth) data

**Parameters:**
- `symbol` (required): Trading pair
- `depth` (optional): Number of price levels (default: 20, max: 200)
- `exchange` (optional): Exchange name

**Example Request:**
```bash
GET http://127.0.0.1:8000/orderbook?symbol=BTC/USDT&depth=5&exchange=binance
```

**Example Response:**
```json
{
  "exchange": "binance",
  "symbol": "BTC/USDT",
  "bids": [
    {"price": 96750.0, "amount": 0.5},
    {"price": 96749.5, "amount": 1.2}
  ],
  "asks": [
    {"price": 96751.0, "amount": 0.6},
    {"price": 96751.5, "amount": 1.1}
  ]
}
```

---

### Endpoint: GET /top_markets

**Description:** Get top trading markets by quote asset

**Parameters:**
- `exchange` (required): Exchange name
- `quote_asset` (optional): Quote currency (default: "USDT")
- `limit` (optional): Number of markets (default: 10, max: 50)

**Example Request:**
```bash
GET http://127.0.0.1:8000/top_markets?exchange=binance&quote_asset=USDT&limit=5
```

**Example Response:**
```json
{
  "exchange": "binance",
  "markets": [
    {
      "symbol": "BTC/USDT",
      "price": 96750.5,
      "quote_asset": "USDT",
      "base_asset": "BTC"
    },
    {
      "symbol": "ETH/USDT",
      "price": 3654.22,
      "quote_asset": "USDT",
      "base_asset": "ETH"
    }
  ]
}
```

---

## 🌟 Key Implementation Highlights

### 1. Exchange Instance Caching
```python
# Prevents slow re-initialization of CCXT exchanges
_exchange_cache: dict[str, Any] = {}

def get_exchange(exchange_name: str) -> ccxt.Exchange:
    if exchange_name not in _exchange_cache:
        _exchange_cache[exchange_name] = getattr(ccxt, exchange_name)()
    return _exchange_cache[exchange_name]
```

### 2. Thread-Safe Caching
```python
class TTLCache:
    def __init__(self, default_ttl_seconds: float = 10.0):
        self._cache: dict = {}
        self._lock = threading.Lock()  # Thread safety
```

### 3. Comprehensive Error Handling
```python
@app.exception_handler(CryptoServerError)
def crypto_exception_handler(request, exc: CryptoServerError):
    if isinstance(exc, ExchangeNotSupportedError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})
    if isinstance(exc, SymbolNotSupportedError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})
    # ... more error types
```

### 4. Pydantic Data Validation
```python
class PriceResponse(BaseModel):
    exchange: str
    symbol: str
    price: float
    timestamp_ms: int
```

---

## 🔒 Best Practices Implemented

### Code Quality
- ✅ Type hints throughout
- ✅ Docstrings for all public functions
- ✅ PEP 8 compliance
- ✅ Modular architecture
- ✅ Separation of concerns

### Security
- ✅ Input validation with Pydantic
- ✅ Environment variable configuration
- ✅ No hardcoded credentials
- ✅ Rate limit error handling

### Performance
- ✅ In-memory caching
- ✅ Exchange instance reuse
- ✅ Async-capable framework (FastAPI)
- ✅ Configurable TTL

### Maintainability
- ✅ Clear project structure
- ✅ Comprehensive documentation
- ✅ Test coverage
- ✅ Error messages with context

---

## 📈 Performance Considerations

### Caching Strategy
- **First Request:** 2-5 seconds (loading exchange markets)
- **Cached Requests:** <100ms (instant response)
- **Cache TTL:** 10 seconds (configurable)

### Rate Limits
- Respects exchange rate limits
- Caching reduces API calls
- Rate limit errors caught and reported

---

## 🛠️ Development Tools Used

- **GitHub Copilot:** AI-assisted coding
- **Claude/ChatGPT:** Design decisions and problem-solving
- **VS Code:** Primary development environment
- **Pytest:** Testing framework
- **FastAPI:** Modern Python web framework
- **CCXT:** Cryptocurrency exchange integration

---

## 📝 Testing Instructions

### Manual Testing

1. **Start the server:**
```bash
cd src
python -m uvicorn mcp_crypto_server.api.app:app --host 127.0.0.1 --port 8000
```

2. **Test endpoints:**
```bash
# Price endpoint
curl "http://127.0.0.1:8000/price?symbol=BTC/USDT&exchange=binance"

# Ticker endpoint
curl "http://127.0.0.1:8000/ticker?symbol=ETH/USDT&exchange=binance"

# OHLCV endpoint
curl "http://127.0.0.1:8000/ohlcv?symbol=BTC/USDT&timeframe=1h&limit=5&exchange=binance"

# Order book endpoint
curl "http://127.0.0.1:8000/orderbook?symbol=BTC/USDT&depth=5&exchange=binance"

# Top markets endpoint
curl "http://127.0.0.1:8000/top_markets?exchange=binance&quote_asset=USDT&limit=5"
```

3. **Interactive API documentation:**
```
http://127.0.0.1:8000/docs
```

---

## 🎯 Assignment Requirements Checklist

### Core Features
- ✅ Real-time cryptocurrency price fetching
- ✅ Historical market data queries
- ✅ Multiple exchange support
- ✅ RESTful API endpoints
- ✅ MCP protocol implementation

### Robustness
- ✅ Comprehensive error handling
- ✅ Input validation
- ✅ Caching mechanism
- ✅ Rate limit management
- ✅ Type safety with Pydantic

### Code Quality
- ✅ Python best practices (PEP 8)
- ✅ Modular architecture
- ✅ Clear documentation
- ✅ Proper project structure
- ✅ Type hints

### Testing
- ✅ Unit tests for cache
- ✅ Integration tests for client
- ✅ MCP tools tests
- ✅ High test coverage
- ✅ Edge case handling

### Documentation
- ✅ README with setup instructions
- ✅ API documentation
- ✅ Code comments
- ✅ Project documentation
- ✅ Usage examples

---

## 🚀 Deployment

### Production Considerations

1. **Environment Variables:**
```bash
# .env file
DEFAULT_EXCHANGE=binance
CACHE_TTL_SECONDS=10
```

2. **Production Server:**
```bash
uvicorn mcp_crypto_server.api.app:app --host 0.0.0.0 --port 8000 --workers 4
```

3. **Docker Support (Future):**
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./src/
CMD ["uvicorn", "mcp_crypto_server.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📞 Support & Contact

For questions or issues:
1. Check the API documentation: `http://127.0.0.1:8000/docs`
2. Review test cases in `tests/` directory
3. Consult README.md for setup instructions

---

## 📄 License

This project is developed as an academic assignment.

---

## 🙏 Acknowledgments

- **CCXT Library:** For unified exchange API
- **FastAPI:** For modern Python web framework
- **GitHub Copilot:** For AI-assisted development
- **Claude/ChatGPT:** For problem-solving assistance

---

**Last Updated:** November 15, 2025
**Version:** 1.0.0
**Python Version:** 3.10+
