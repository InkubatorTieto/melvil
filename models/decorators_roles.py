from functools import wraps

from flask import flash, redirect, session, url_for

from models.users import User

# README
# Use parenthesis when you use these decorators
#
# GOOD
# @library.route("/")
# @require_role()
# def index():
#     ...
#
# BAD
# @library.route("/")
# @require_role
# def index():
#     ...


def require_logged_in(
        redirect_page="library.login",
        show_login_required_message=True):
    def decorator(func):
        @wraps(func)
        def inner_func(*args, **kwargs):
            login_required_msg = "Please, login first to access this page!"

            if "logged_in" in session and session["logged_in"]:
                return func(*args, **kwargs)

            if show_login_required_message:
                flash(login_required_msg)

            return redirect(url_for(redirect_page))

        return inner_func

    return decorator


def require_not_logged_in(redirect_page="library.index"):
    def decorator(func):
        @wraps(func)
        def inner_func(*args, **kwargs):
            if not ("logged_in" in session):
                return func(*args, **kwargs)
            elif not (session["logged_in"]):
                return func(*args, **kwargs)
            else:
                return redirect(url_for(redirect_page))

        return inner_func

    return decorator


def require_role(role="USER", redirect_page="library.index"):
    def decorator(func):
        @wraps(func)
        def inner_func(*args, **kwargs):
            not_authorized_msg = "You are not authorized to access this page!"
            if "id" in session:
                user = User.query.get(session["id"])
                if user.has_role(role):
                    return func(*args, **kwargs)
                else:
                    flash(not_authorized_msg)
                    return redirect(url_for(redirect_page))
            else:
                flash(not_authorized_msg)
                return redirect(url_for(redirect_page))

        return inner_func

    return decorator
