import pytest
from main import create_app


@pytest.fixture
def app():
    """Create a Flask app for testing."""
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    with app.test_client() as client:
        yield client 