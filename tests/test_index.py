from flask import url_for


def test_app(app):
    client = app.test_client()
    resp = client.get(url_for('library.index'))
    assert resp.status_code == 200


def test_config_access(config):
    assert config['SECRET_KEY'] == 24


def test_login(user):
    data = {
        'email': user['email'],
        'password': user['password']
    }
    resp = user['client'].get(url_for('library.login'), data=data)
    assert resp.status_code == 200

    resp = user['client'].post(url_for('library.login'), data=data)
    assert resp.status_code == 200


def test_registration(user):
    assert True
