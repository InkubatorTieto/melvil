from models.decorators_roles import (
    require_logged_in,
    require_not_logged_in,
    require_role
)
from flask import session
import pytest


@pytest.mark.parametrize('login', [True, False, None])
@pytest.mark.parametrize('redirect_page', [None, 'library.index'])
def test_require_logged_in(login, redirect_page):

    session['logged_in'] = login

    if session['logged_in'] is None:
        del session['logged_in']

    def modify_redirect(page):
        if page:
            return page
        else:
            pass

    @require_logged_in(modify_redirect(redirect_page))
    def func_logged_in():
        return 'ok'

    @require_not_logged_in(modify_redirect(redirect_page))
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
