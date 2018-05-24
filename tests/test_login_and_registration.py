from flask import url_for, session


def test_login(user):
    data = {
        'email': user['email'],
        'password': user['password']
    }
    resp = user['client'].get(url_for('library.login'), data=data)
    assert resp.status_code == 200

    resp = user['client'].post(url_for('library.login'), data=data)
    assert resp.status_code == 200


    # assert resp.session['logged_in'] == True
    # session = request.node
    # print(session)
    # assert session['logged_in'] == True
    # assert session['id'] is not None
    # assert session['email'] == user['email']


def test_registration(user):
    assert True
