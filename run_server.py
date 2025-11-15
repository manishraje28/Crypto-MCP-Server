"""Quick runner script to start the FastAPI server."""
import sys
from pathlib import Path

# Add src to path
ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "mcp_crypto_server.api.app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=[str(SRC)]
    )
