from flask import url_for


def test_contact(user, client):

    data = {
        'email': user['email'],
        'title': user['title'],
        'message': user['message']
    }
    resp = client.get(url_for('library.contact'))
    assert resp.status_code == 200

    resp = client.post(url_for('library.contact'), data=data)
    assert resp.status_code == 200

    print(user)
    assert True
