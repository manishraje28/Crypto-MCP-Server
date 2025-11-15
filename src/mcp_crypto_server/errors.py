class CryptoServerError(Exception):
    """Base exception class for the crypto MCP server."""


class ExchangeNotSupportedError(CryptoServerError):
    """Raised when a requested exchange is not available."""


class SymbolNotSupportedError(CryptoServerError):
    """Raised when a requested symbol is not available on an exchange."""


class RateLimitError(CryptoServerError):
    """Raised when upstream API rate limits are hit."""


class UpstreamAPIError(CryptoServerError):
    """Generic wrapper for unexpected errors from external services."""


def user_friendly_message(exc: Exception) -> str:
    """Convert internal errors into safe messages for the LLM/client."""
    if isinstance(exc, ExchangeNotSupportedError):
        return f"Exchange not supported: {exc}"
    if isinstance(exc, SymbolNotSupportedError):
        return f"Symbol not supported on this exchange: {exc}"
    if isinstance(exc, RateLimitError):
        return "Upstream API rate limit exceeded. Please retry after some time."
    if isinstance(exc, UpstreamAPIError):
        return f"Upstream API error: {exc}"
    return f"Unexpected error: {exc}"
