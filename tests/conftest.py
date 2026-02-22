import pytest
from pathlib import Path
import sys


# # Add app to path
# sys.path.insert(0, str(Path(__file__).parent.parent))

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


from fastapi.testclient import TestClient
from app.main import app



@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(scope="session")
def test_config():
    """Provide test configuration"""
    return {
        "test_features": [1.0, 2.0, 3.0, 4.0],
        "expected_output_type": (float, int, dict),
    }


@pytest.fixture
def sample_payload(test_config):
    """Provide sample test payload"""
    return {"features": test_config["test_features"]}