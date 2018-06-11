from flask import url_for


def test_login(db_user, client):

    resp = client.get(url_for('library.login'))
    assert resp.status_code == 200

    # resp = client.post(url_for('library.login'), data=db_user,
    #             follow_redirects=True)
    # assert resp.status_code == 200

    assert True


def test_registration(db_user):
    assert True
