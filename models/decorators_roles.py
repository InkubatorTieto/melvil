from flask import session, redirect, url_for
from functools import wraps
from models.users import User


def require_logged_in(redirect_page='library.login'):

    def decorator(func):

        @wraps(func)
        def inner_func(*args, **kwargs):

            if session and 'logged_in' in session:
                return func(*args, **kwargs)
            else:
                return redirect(url_for(redirect_page))
        return inner_func

    return decorator


def require_not_logged_in(redirect_page='library.index'):

    def decorator(func):

        @wraps(func)
        def inner_func(*args, **kwargs):

            if not(session and 'logged_in' in session):
                return func(*args, **kwargs)
            else:
                return redirect(url_for(redirect_page))
        return inner_func

    return decorator


def require_role(role='USER', redirect_page='library.index'):

    def decorator(func):

        @wraps(func)
        def inner_func(*args, **kwargs):

            try:
                user_email = session['email']
                role_in_db = User.query.filter_by(email=user_email).first()
                print(role_in_db.roles[0])
                print('Role: '+role)
                if 'Role: '+role == role_in_db.roles[0]:
                    return func(*args, **kwargs)
                else:
                    return redirect(url_for(redirect_page))
            except:
                return redirect(url_for(redirect_page))

        return inner_func
    return decorator


