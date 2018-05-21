def test_app(app):
    client = app.test_client()
    resp = client.get('/search')
    assert resp.status_code == 200