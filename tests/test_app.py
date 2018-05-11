def test_index(app):
    with app.test_client() as client:
        resp = client.get('/')
        assert resp.status_code == 200
