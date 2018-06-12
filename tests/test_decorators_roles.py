from models.decorators_roles import (
    require_logged_in,
    require_not_logged_in,
    require_role
)
from flask import session
import pytest
from models.users import User, Role, RoleEnum
from mimesis import Generic
from init_db import db


g = Generic('en')


@pytest.mark.parametrize('login', [True, False, None])
def test_login_decorators(login):

    session['logged_in'] = login

    if session['logged_in'] is None:
        del session['logged_in']

    @require_logged_in()
    def func_logged_in():
        return 'ok'

    @require_not_logged_in()
    def func_not_logged_in():
        return 'ok'

    if login:
        if func_logged_in() != 'ok' and func_not_logged_in() == 'ok':
            assert False
    else:
        if func_logged_in() == 'ok' and func_not_logged_in() != 'ok':
            assert False


@pytest.mark.parametrize('login', [True, False, None])
@pytest.mark.parametrize('redirect_page', ['library.index'])
def test_login_decorators_custom_redirect(login, redirect_page):

    session['logged_in'] = login

    if session['logged_in'] is None:
        del session['logged_in']

    @require_logged_in(redirect_page)
    def func_logged_in():
        return 'ok'

    @require_not_logged_in(redirect_page)
    def func_not_logged_in():
        return 'ok'

    if login:
        if func_logged_in() == 'ok' and func_not_logged_in() != 'ok':
            assert True
        else:
            assert False
    else:
        if func_logged_in() != 'ok' and func_not_logged_in() == 'ok':
            assert True
        else:
            assert False


@pytest.mark.parametrize('role', ['USER', 'ADMIN'])
@pytest.mark.parametrize('required_role', ['USER', 'ADMIN'])
def test_role_decorator(role, required_role):
    email = g.person.email()
    new_user = User(
        email=email,
        first_name=g.person.name(),
        surname=g.person.surname(),
        password_hash=g.cryptographic.hash(),
        active=g.development.boolean(),
    )
    db.session.add(new_user)
    db.session.commit()

    data = User.query.filter_by(email=email).first()
    data.roles[0] = Role(name=role)

    db.session.commit()

    session['logged_in'] = True
    session['id'] = data.id
    session['email'] = data.email

    @require_role(role=required_role)
    def func_role():
        return 'ok'

    print(func_role(), data.roles)

    if role == required_role:
        if func_role() != 'ok':
            assert False
    else:
        if func_role() == 'ok':
            assert False


