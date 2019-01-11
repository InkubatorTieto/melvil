from flask import g, session
from flask_simpleldap import LDAP

from models.users import User


ldap_client = LDAP()


def register_hooks(app):
    @app.before_request
    def before_request():
        g.user = None
        if 'username' in session:
            session['logged_in'] = True
            # This is where you'd query your database to get the user info.
            user = User.query.filter_by(
                username=session['username']).first().username
            g.user = user
            # Create a global with the LDAP groups the user is a member of.
            g.ldap_groups = ldap_client.get_user_groups(
                user=session['username'])


def refine_data(object, data_tag):
    out = object[data_tag][0].decode('utf8')
    return out
