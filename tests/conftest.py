import pytest
from app import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config['SECRET_KEY'] = 24
    return app
