from models.users import User, Role
from models.library import RentalLog
from models.books import Book, Copy, Author, Tag


def test_user(session):
    user1 = User(email='user1@test.com')
    user2 = User(email='user2@test.com')
    session.add(user1)
    session.add(user2)
    session.commit()
    assert len(User.query.all()) > 1


def test_role(session):
    role1 = Role(name='Admin')
    role2 = Role(name='User')
    session.add(role1)
    session.add(role2)
    assert len(Role.query.all()) == 2
