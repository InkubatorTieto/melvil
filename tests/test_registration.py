from flask import url_for
from models import User


def test_registration_status_code_for_get(client, registration_form):
    resp = client.get(url_for('library.registration'),
                      data=registration_form.data,
                      follow_redirects=True)
    assert resp.status_code == 200, \
        "Registration view, GET request gives wrong response"


def test_registration_valid_data_inserted(client, session, registration_form):
    resp = client.post(url_for('library.registration'),
                       data=registration_form.data,
                       follow_redirects=True)

    assert resp.status_code == 200, \
        "Registration view, POST request gives wrong response"

    user = User.query.filter_by(email=registration_form.email.data).first()
    assert user is not None, \
        "Registration view, user with valid data couldn't register"
    if user:
        session.delete(user)
        session.commit()


def test_registration_invalid_data_inserted(client,
                                            session,
                                            registration_form_invalid):
    client.post(url_for('library.registration'),
                data=registration_form_invalid.data,
                follow_redirects=True)
    user = User.query\
        .filter_by(email=registration_form_invalid.email.data).first()
    assert user is None, \
        "Registration view, user with invalid data registered"
    if user:
        session.delete(user)
        session.commit()


def test_registration_data_registered_user(client,
                                           session,
                                           registration_form_registered_user):
    client.post(url_for('library.registration'),
                data=registration_form_registered_user.data,
                follow_redirects=True)
    user = User.query.\
        filter_by(email=registration_form_registered_user.email.data).count()
    assert user == 1, \
        "Registration view, user registered twice"
    if user > 1:
        user = User.query\
            .filter_by(email=registration_form_registered_user.email.data)\
            .all()
        session.delete(user[1])
        session.commit()
