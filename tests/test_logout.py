from flask import url_for
from flask import session


def test_logout_status_code_for_get(client):
    resp = client.get(url_for('library.logout'),
                      follow_redirects=True)
    assert resp.status_code == 200, \
        "Logout, GET request gives wrong response"


def test_logout_logging_out_user(app, login_form):
    with app.test_client() as c:
        session['logged_in'] = False
        c.post(url_for('library.login'),
               data=login_form.data)
        assert session['logged_in'] is True, \
            "Login view, user with valid data hasn't logged in"
        c.get(url_for('library.logout'))
        assert 'logged_in' not in session, \
            "Logout, user couldn't log out"
        session.clear()
