from flask import url_for


def test_reset_password_status_code_for_get(client):
    resp = client.get(url_for('library.reset'),
                      follow_redirects=True)
    assert resp.status_code == 200, \
        "Reset password view, GET request gives wrong response"


def test_reset_password_status_code_for_post(client, forgot_pass):
    resp = client.post(url_for('library.reset'),
                       data=forgot_pass.data)
    assert resp.status_code == 200, \
        "Registration view, POST request gives wrong response"
