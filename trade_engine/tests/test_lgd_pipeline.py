import unittest
import sys
from pathlib import Path

# Add repo root to path
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tests.test_lgd_pipeline import TestLGDB2BPipeline

if __name__ == "__main__":
    unittest.main()
