from flask import url_for


def test_reset_password_status_code_for_get(client):
    resp = client.get(url_for('library.reset'),
                      follow_redirects=True)
    assert resp.status_code == 200, \
        "Reset password GET view wrong response"
