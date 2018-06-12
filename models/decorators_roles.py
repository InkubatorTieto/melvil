from flask import session, redirect, url_for
from functools import wraps
from models.users import User


def require_logged_in(redirect_page='library.login'):

    def decorator(func):

        @wraps(func)
        def inner_func(*args, **kwargs):

            if 'logged_in' in session:

                if session['logged_in']:
                    return func(*args, **kwargs)
                else:
                    return redirect(url_for(redirect_page))

            else:
                return redirect(url_for(redirect_page))

        return inner_func

    return decorator


def require_not_logged_in(redirect_page='library.index'):

    def decorator(func):

        @wraps(func)
        def inner_func(*args, **kwargs):

            if not('logged_in' in session):
                return func(*args, **kwargs)
            elif not(session['logged_in']):
                return func(*args, **kwargs)
            else:
                return redirect(url_for(redirect_page))

        return inner_func

    return decorator


def require_role(role='USER', redirect_page='library.index'):

    def decorator(func):

        @wraps(func)
        def inner_func(*args, **kwargs):

            if 'id' in session:
                user = User.query.get(session['id'])

                if user.has_role(role):
                    return func(*args, **kwargs)
                else:
                    return redirect(url_for(redirect_page))

            else:
                return redirect(url_for(redirect_page))

        return inner_func
    return decorator
