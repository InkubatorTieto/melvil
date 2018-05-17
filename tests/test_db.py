from models.users import Role
from tests.populate import *

role1 = Role(name='ADMIN')
role2 = Role(name='USER')


def test_user(session):

    # session.add_all([user1, user2])
    users = populate_users()
    session.add_all(users)
    session.commit()

    assert len(User.query.all()) > 1
    # print(User.query.all())

    session.add(role1)
    session.add(role2)
    assert len(Role.query.all()) == 2

    user = User.query.all()
    # role = Role.query.filter_by(name='ADMIN').first()

    # user.roles.append(role)

    # print('U: ', user)
    # print('R: ', role.users)

    books = populate_books()
    session.add_all(books)
    session.commit()
    # print('B: ', Book.query.all())

    authors = populate_authors()
    session.add_all(authors)
    session.commit()
