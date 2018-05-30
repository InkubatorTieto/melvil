from flask import url_for


def test_login(user, client):
    #
    data = {
        'email': user['email'],
        'password': user['password']
    }
    resp = client.get(url_for('library.login'))
    assert resp.status_code == 200
    #
    resp = client.post(url_for('library.login'), data=data)
    assert resp.status_code == 200

    print(user)
    assert True


def test_registration(user):
    assert True
