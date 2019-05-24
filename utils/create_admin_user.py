from werkzeug.security import generate_password_hash
import re

from forms.custom_validators import email_regex
from models.users import User, Role, RoleEnum
from init_db import db


def create_super_user():
    email_data = input("What is your email: ")
    print("Introduce yourself:\n")
    first_name = input("First name: ")
    surname = input("Surname: ")
    password = input("Password: ")
    password_2 = input("Password: ")
    if User.query.filter_by(email=email_data).first():
        return print("This e-mail already exists in the database!")
    if not re.compile(email_regex()).match(email_data):
        return print("Only Tieto emails are accepted!")
    if password != password_2:
        return print("Passwords are not the same!")
    new_user = User(
        email=email_data,
        first_name=first_name,
        surname=surname,
        password_hash=generate_password_hash(
            password),
        active=True

    )
    db.session.add(new_user)
    db.session.commit()

    user = User.query.filter_by(id=new_user.id).first()
    role = Role.query.filter_by(name=RoleEnum.USER).first()
    user.roles.remove(role)
    role = Role.query.filter_by(name=RoleEnum.ADMIN).first()
    user.roles.append(role)
    db.session.commit()
    print("Success!")
