import sys
from pathlib import Path

# FIX: Configure pytest path resolution (I reported ModuleNotFoundError, agent added conftest.py)
# Pytest automatically loads conftest.py to fix import resolution for tests/
sys.path.insert(0, str(Path(__file__).parent.parent))
