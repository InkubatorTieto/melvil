from flask import url_for


def test_status_code(client, app_session, db_copies):
    resp = client.get(url_for('library.reserve',
                              copy_id=db_copies[1].id))
    assert resp.status_code == 302
