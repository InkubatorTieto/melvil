from random import randint

from sqlalchemy import func

from tests.populate import *
from models import *


def test_users(session):
    role_admin = Role(name='ADMIN')
    role_user = Role(name='USER')
    session.add_all([role_admin, role_user])
    session.commit()
    assert Role.query.count() == 2, "db does not contain 2 roles"

    users = populate_users(n=10)
    session.add_all(users)
    session.commit()

    assert User.query.count() == 10, "db does not contain 10 Users"

    users = User.query.all()
    for u in users:
        u.roles.append(role_user)
        assert u.roles != [], "role not added to user"


def test_books(session):
    authors = populate_authors(n=5)
    session.add_all(authors)
    session.commit()
    assert Author.query.count() == 5, "db does not contain 5 authors"

    tags = populate_tags(n=10)
    session.add_all(tags)
    session.commit()
    assert Tag.query.count() == 10, "db does not contain 10 tags"

    for a in Author.query.all():
        books = populate_books(n=a.id, authors=[a])
        session.add_all(books)
        session.commit()
        for b in books:
            assert a in b.authors, "authors not added to book authors field"
            copies = populate_copies(b, n=randint(1, 3))
            session.add_all(copies)
            for c in copies:
                assert c in b.copies, "copies not added to book copies field"
                assert c.book is b, "copy reference to book is wrong"
        session.commit()

        assert Book.query.filter(Book.authors.contains(a)).count() == a.id

    for t in Tag.query.all():
        book = Book.query.order_by(func.random()).first()
        book.tags.append(t)
        session.commit()
        assert t.books != [], "tags book field is empty"
        assert t in book.tags, "tags not added to book tags field"


def test_library(session):
    b = Book.query.order_by(func.random()).first()
    u = User.query.order_by(func.random()).first()
    logs = populate_rental_logs(b.id, u.id, n=1)
    session.add_all(logs)
    session.commit()
    print(RentalLog.query.all())
    assert RentalLog.book_copy_id != [], "rental log does not contain book id"
    assert RentalLog.user_id != [], "rental log does not contain user id"
