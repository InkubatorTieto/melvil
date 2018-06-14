from flask import url_for
from models import User
from werkzeug.security import check_password_hash
import pytest


def test_login(view_login, client):
    resp = client.get(url_for('library.login'))
    assert resp.status_code == 200

    resp = client.post(url_for('library.login'), data=view_login.data,
                       follow_redirects=True)
    assert resp.status_code == 200


def test_registration(view_registration, client):
    assert view_registration.password.data == view_registration.confirm_pass.data, \
        "Field password and confirm password are not the same "

    resp = client.post(url_for('library.registration'), data=view_registration.data,
                       follow_redirects=True)
    assert resp.status_code == 200

    user = User.query.filter_by(email=view_registration.email.data).first()
    assert user, "Data validation failed"
    assert view_registration.email.data == user.email, \
        "Email is not the same as given at the entrance"
    assert view_registration.first_name.data == user.first_name, \
        "First name is not the same as given at the entrance"
    assert view_registration.surname.data == user.surname, \
        "Last name is not the same as given at the entrance"
    assert check_password_hash(user.password_hash, view_registration.password.data), \
        "Last name is not the same as given at the entrance"


@pytest.mark.parametrize("values, result", [
    ("asdac.asd@tieto.com", True),
    ("@tietc.com", False),
    ("asdac.asd@o2.com", False)

])
def test_name(view_registration, values, result):
    view_registration.email.data = values
    view_registration.email.validate(view_registration)
    assert bool(view_registration.errors) != result, \
        "The validator 'tieto_email' returns not" \
        " a valid value\n Errors:{0}".format(view_registration.errors)


@pytest.mark.parametrize("values, result", [
    ("Paweł", True),
    ("Żźćńęśńóąę", True),
    ("asdac.asd@o2", False),
    ("P.aweł", False),
    ("pawel", False)
])
def test_name(view_registration, values, result):
    view_registration.first_name.data = values
    view_registration.first_name.validate(view_registration)
    assert bool(view_registration.errors) != result, \
        "The validator 'name' returns not" \
        " a valid value\n Errors:{0}".format(view_registration.errors)


@pytest.mark.parametrize("values, result", [
    ("Paweł", True),
    ("Żźćńęśńóąę", True),
    ("asdac.asd@o2", False),
    ("P.aweł", False),
    ("pawel", False),
    ("Żasdfźćńęśńóąę-Ążźćńęśńóąę", True),
    ("Żasdfźćńęśńóąę Ążźćńęśńóąę", True)
])
def test_surname(view_registration, values, result):
    view_registration.surname.data = values
    view_registration.surname.validate(view_registration)
    assert bool(view_registration.errors) != result, \
        "The validator 'surname' returns not" \
        " a valid value\n Errors:{0}".format(view_registration.errors)


@pytest.mark.parametrize("values, result", [
    ("Pawełdsa", False),
    ("Żźćńęśńóąę", False),
    # ("asdac.asd@o2", False),
    ("P.awełasd", False),
    ("pawelasd", False),
    ("!123pasa", False),
    ("#123Pas8", True)
])
def test_check_password(view_registration, values, result):
    view_registration.password.data = values
    view_registration.confirm_pass.data = values
    view_registration.password.validate(view_registration)
    assert bool(view_registration.errors) != result, \
        "The validator 'password' returns not" \
        " a valid value\n Errors:{0}".format(view_registration.errors)
