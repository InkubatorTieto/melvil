def test_app(app):
    resp = app.test_client()
    assert resp
