import os
import sys
from pathlib import Path


# Ensure the `src` folder is on sys.path so tests can import the package and
# the local `ccxt` shim without needing an editable install.
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
