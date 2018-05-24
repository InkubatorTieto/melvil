import pytest
from app import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config['SECRET_KEY'] = 24
    return app


@pytest.fixture
def user(app):
    app = create_app()
    client = app.test_client()
    data = {
        'email': 'test1@test.com',
        'first_name': 'Testowy',
        'surname': 'test',
        'password': '5354',
        'client': client}
    return data

