from random import randint
from sqlalchemy import func

from tests.populate import (
    populate_users,
    populate_copies,
    populate_tags,
    populate_authors,
    populate_books,
    populate_rental_logs,
    populate_magazines
)
from models import (
    Role,
    User,
    Author,
    Tag,
    Book,
    Copy,
    LibraryItem,
    Magazine,
    RentalLog)


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

    for a in Author.query.all():
        books = populate_books(n=a.id, authors=[a])
        session.add_all(books)
        session.commit()
        for b in books:
            assert a in b.authors, "authors not added to book authors field"

            copies = populate_copies(b, n=randint(1, 3))
            session.add_all(copies)
            session.commit()
            for c in copies:
                assert c in b.copies, "copy not added to book copy field"
                assert c.library_item is b, "copy reference to book is wrong"
        session.commit()

        assert Book.query.filter(Book.authors.contains(a)).count() == a.id


def test_magazine(session):
    magazines = populate_magazines()
    session.add_all(magazines)
    session.commit()
    assert Magazine.query.count() == 10, "db does not contain 10 magazines"

    for m in magazines:
        copies = populate_copies(m, n=randint(1, 2))
        session.add_all(copies)
        session.commit()
        for c in copies:
            assert c in m.copies, "copy not added to magazine copy field"
            assert c.library_item is m, "copy reference to magazine is wrong"
        session.commit()


def test_library(session):
    tags = populate_tags(n=10)
    session.add_all(tags)
    session.commit()
    assert Tag.query.count() == 10, "db does not contain 10 tags"

    for t in Tag.query.all():
        book = Book.query.order_by(func.random()).first()
        book.tags.append(t)
        session.commit()
        assert t.library_items != [], "tags item field is empty"
        assert t in book.tags, "tags not added to book tags field"

    c = Copy.query.order_by(func.random()).first()
    u = User.query.order_by(func.random()).first()
    log = populate_rental_logs(c.id, u.id, n=1)[0]
    session.add(log)
    session.commit()
    assert log.copy_id == c.id, "rental log has wrong copy id"
    assert log.user_id == u.id, "rental log has wrong user id"

    i = LibraryItem.query.get(c.library_item_id)
    assert log.copy in i.copies, "copy relates to wrong item"


def test_delete(session):
    logs = []

    copies = Copy.query.order_by(func.random()).limit(3).all()
    users = User.query.order_by(func.random()).limit(3).all()
    for i in range(3):
        log = populate_rental_logs(copies[i].id, users[i].id, n=1)[0]
        session.add(log)
        session.commit()
        logs.append(log)
    num_users = User.query.count()
    num_copies = Copy.query.count()
    num_logs = RentalLog.query.count()

    session.delete(users[0])
    session.commit()
    num_users = num_users - 1
    assert User.query.count() == num_users, \
        "number of users after User delete is wrong"
    assert Copy.query.count() == num_copies, \
        "number of copies after User delete is wrong"
    num_logs = num_logs - 1
    assert RentalLog.query.count() == num_logs, \
        "number of rental logs after User delete is wrong"

    session.delete(copies[1])
    session.commit()
    assert User.query.count() == num_users, \
        "number of users after Copy delete is wrong"
    num_copies = num_copies - 1
    assert Copy.query.count() == num_copies, \
        "number of copies after Copy delete is wrong"
    num_logs = num_logs - 1
    assert RentalLog.query.count() == num_logs, \
        "number of rental logs after Copy delete is wrong"

    session.delete(logs[2])
    session.commit()
    assert User.query.count() == num_users, \
        "number of users after RentalLog delete is wrong"
    assert Copy.query.count() == num_copies, \
        "number of copies after RentalLog delete is wrong"
    num_logs = num_logs - 1
    assert RentalLog.query.count() == num_logs, \
        "number of rental logs after RentalLog delete is wrong"

    b = Book.query.order_by(func.random()).first()
    m = Magazine.query.order_by(func.random()).first()
    t = Tag.query.order_by(func.random()).first()

    num_books = Book.query.count()
    num_magazines = Magazine.query.count()
    num_tags = Tag.query.count()
    num_copies = Copy.query.count()

    session.delete(t)
    session.commit()
    assert Book.query.count() == num_books, \
        "number of books after Tag delete is wrong"
    assert Magazine.query.count() == num_magazines, \
        "number of magazines after Tag delete is wrong"
    num_tags = num_tags - 1
    assert Tag.query.count() == num_tags, \
        "number of tags after Tag delete is wrong"

    copy_b = b.copies[0].id
    session.delete(b)
    session.commit()
    num_books = num_books - 1
    assert Book.query.count() == num_books, \
        "number of books after Book delete is wrong"
    assert Magazine.query.count() == num_magazines, \
        "number of magazines after Book delete is wrong"
    assert Tag.query.count() == num_tags, \
        "number of tags after Book delete is wrong"
    num_copies = num_copies - len(b.copies)
    assert Copy.query.count() == num_copies, \
        "number of copies after Book delete is wrong"
    assert Copy.query.get(copy_b) is None, \
        "there are remaining copies without book parent"

    copy_m = m.copies[0].id
    session.delete(m)
    session.commit()
    assert Book.query.count() == num_books, \
        "number of books after Magazine delete is wrong"
    num_magazines = num_magazines - 1
    assert Magazine.query.count() == num_magazines, \
        "number of magazines after Magazine delete is wrong"
    assert Tag.query.count() == num_tags, \
        "number of tags after Magazine delete is wrong"
    num_copies = num_copies - len(m.copies)
    assert Copy.query.count() == num_copies, \
        "number of copies after Magazine delete is wrong"
    assert Copy.query.get(copy_m) is None, \
        "there are remaining copies without magazine parent"
