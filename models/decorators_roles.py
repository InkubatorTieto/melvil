from flask import session, request, redirect, url_for


def require_logged_in(func):

    def check(*args, **kwargs):

        if session and 'logged_in' in session:
            return func(*args, **kwargs)
        else:
            redirect(url_for('library.index'))

    return check
