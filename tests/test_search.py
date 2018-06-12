from flask import url_for


def test_search(session, client):
    #
    resp = client.get(url_for('library.search'))
    assert resp.status_code == 200
