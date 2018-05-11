def test_app(app):
    client = app.test_client()
    resp = client.get('/')
    assert resp.status_code == 200
