from unittest import mock

from flask import url_for
from flask import session


def test_login_status_code_for_get(client, login_form, mock_ldap):
    with mock.patch('views.index.ldap_client', mock_ldap):
        resp = client.get(url_for('library.login'), data=login_form.data)
        assert resp.status_code == 200, \
            "Login view, GET request gives wrong response"


def test_login_status_code_for_post(client, login_form):
    resp = client.post(url_for('library.login'),
                       data=login_form.data)
    assert resp.status_code == 200, \
        "Login view, POST request gives wrong response"


def test_login_valid_data_inserted(login_form, mock_ldap, app):
    with app.test_client() as c, mock.patch(
        'views.index.ldap_client', mock_ldap
    ):
        session['logged_in'] = False
        c.post(url_for('library.login'), data=login_form.data)
        assert session['logged_in'] is True, \
            "Login view, user with valid data hasn't logged in"
        session.clear()


def test_login_invalid_data_inserted(app, login_form_invalid, mock_ldap):
    with app.test_client() as c, mock.patch(
        'views.index.ldap_client', mock_ldap
    ):
        session['logged_in'] = False
        c.post(url_for('library.login'),
               data=login_form_invalid.data)
        assert 'logged_in' not in session, \
            "Login view, user with invalid data logged in"
        session.clear()
