from tests.populate import *
from models import *

role1 = Role(name='ADMIN')
role2 = Role(name='USER')


def test_user(session):
    session.add(role1)
    session.add(role2)
    session.commit()
    assert Role.query.count() == 2

    users = populate_users(n=10)
    session.add_all(users)
    session.commit()

    assert User.query.count() == 10, "database does not contain 10 Users"
    # print(User.query.all())

    users = User.query.all()
    for u in users:
        assert u.roles == []


def test_books(session):
    authors = populate_authors(n=5)
    session.add_all(authors)
    session.commit()
    assert Author.query.count() == 5

    for a in Author.query.all():
        books = populate_books(n=a.id, authors=[a])
        session.add_all(books)
        session.commit()

        assert Book.query.filter(Book.authors.contains(a)).count() == a.id

