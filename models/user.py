from flask_user import UserMixin
from app import db


class User(db.Model, UserMixin):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    first_name = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    password_hash = db.deferred(db.Column(db.String(128)))
    active = db.Column(db.Boolean)
    roles = db.relationship('Role', secondary='user_roles',
                            lazy='select', backref='users')

    def __init__(self, email):
        self.email = email


class UserRoles(db.Model):

    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id',
                        ondelete='CASCADE'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id',
                        ondelete='CASCADE'))


class Role(db.Model):

    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)  # EMUM
