from flask_user import UserMixin
from app import db
import enum

user_roles = db.Table('user_roles',
                      db.Column('user_id',
                                db.Integer,
                                db.ForeignKey('users.id', ondelete='CASCADE'),
                                primary_key=True),
                      db.Column('role_id',
                                db.Integer,
                                db.ForeignKey('roles.id', ondelete='CASCADE'),
                                primary_key=True))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    first_name = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    password_hash = db.deferred(db.Column(db.String(128)))
    active = db.Column(db.Boolean)
    roles = db.relationship('Role',
                            secondary=user_roles,
                            lazy='select',
                            backref=db.backref('users', lazy='select'))
    rental_logs = db.relationship('RentalLog',
                                  backref=db.backref('user',
                                                     uselist=False,
                                                     single_parent=True,
                                                     lazy='joined'),
                                  lazy='dynamic',
                                  cascade='all, delete-orphan')

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.surname)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return "<User: {} {} role={}>". \
            format(self.first_name, self.surname, self.roles)


class RoleEnum(enum.Enum):
    ADMIN = 0
    USER = 1

    def __str__(self):
        return self.name


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum(RoleEnum), unique=True)

    def __repr__(self):
        return "Role: {}".format(self.name)
