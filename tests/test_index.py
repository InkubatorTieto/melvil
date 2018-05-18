def test_app(app):
    client = app.test_client()
    resp = client.get('/')
    assert resp.status_code == 200



def test_config_access(config):
    assert config['SECRET_KEY'] == 24
