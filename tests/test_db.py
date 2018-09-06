from datetime import datetime
from random import randint

from mimesis import Generic
import pytz
from sqlalchemy import func

from models import (
    User,
    Author,
    Tag,
    Book,
    Copy,
    LibraryItem,
    Magazine,
    RentalLog,
)
from models.library import BookStatus
from models.users import RoleEnum, Role
from tests.populate import (
    populate_users,
    populate_copies,
    populate_tags,
    populate_authors,
    populate_books,
    populate_rental_logs,
    populate_magazines,
)


def test_users(session):
    users = populate_users(n=10)
    session.add_all(users)
    session.commit()
    role_admin = Role.query.filter_by(name=RoleEnum.ADMIN).first()
    user_admin = User.query.order_by(func.random()).first()
    user_admin.roles.append(role_admin)
    session.add(user_admin)
    session.commit()

    for u in users:
        assert u.roles is not None, "role not added to user"


def test_books(session):
    before_authors_count = Author.query.count()
    authors = populate_authors(n=5)
    session.add_all(authors)
    session.commit()
    assert (
        Author.query.count() - before_authors_count == 5
    ), "more/less than 5 authors added"

    for a in authors:
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
    before_magazines_count = Magazine.query.count()
    magazines = populate_magazines()
    session.add_all(magazines)
    session.commit()
    assert (
        Magazine.query.count() - before_magazines_count == 10
    ), "more/less than 10 magazines added"

    for m in magazines:
        copies = populate_copies(m, n=randint(1, 2))
        session.add_all(copies)
        session.commit()
        for c in copies:
            assert c in m.copies, "copy not added to magazine copy field"
            assert c.library_item is m, "copy reference to magazine is wrong"
        session.commit()


def test_library(session):
    before_tag_count = Tag.query.count()
    tags = populate_tags(n=10)
    session.add_all(tags)
    session.commit()
    assert (
        Tag.query.count() - before_tag_count == 10
    ), "more/less than 10 tags added"

    for t in tags:
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


def test_delete_user(session, db_user, db_book):
    g = Generic("en")
    user_id = db_user.id
    copy = Copy(
        asset_code="{}{}".format(
            g.code.locale_code()[:2], g.code.pin(mask="######")
        ),
        library_item=db_book,
        shelf=g.code.pin(),
        has_cd_disk=g.development.boolean(),
    )
    session.add(copy)
    session.commit()
    log = RentalLog(
        copy_id=copy.id,
        user_id=user_id,
        borrow_time=datetime.now(tz=pytz.utc),
        return_time=datetime.now(tz=pytz.utc),
        book_status=BookStatus.BORROWED,
    )
    session.add(log)
    session.commit()

    assert User.query.get(user_id) is not None, "User add failed"
    assert (
        RentalLog.query.filter_by(user_id=user_id).count() == 1
    ), "RentalLog add failed"
    assert (
        Copy.query.filter_by(library_item=db_book).count() == 1
    ), "Copy add failed"

    session.delete(db_user)
    session.commit()

    assert User.query.get(user_id) is None, "User delete failed"
    assert (
        RentalLog.query.filter_by(user_id=user_id).count() == 0
    ), "RentalLog was not deleted with the User"
    assert (
        Copy.query.filter_by(library_item=db_book).count() == 1
    ), "Copy got deleted with the User"


def test_delete_book(session, db_user, db_book):
    g = Generic("en")
    user_id = db_user.id
    copy = Copy(
        asset_code="{}{}".format(
            g.code.locale_code()[:2], g.code.pin(mask="######")
        ),
        library_item=db_book,
        shelf=g.code.pin(),
        has_cd_disk=g.development.boolean(),
    )
    session.add(copy)
    session.commit()
    log = RentalLog(
        copy_id=copy.id,
        user_id=user_id,
        borrow_time=datetime.now(tz=pytz.utc),
        return_time=datetime.now(tz=pytz.utc),
        book_status=BookStatus.BORROWED,
    )
    session.add(log)
    session.commit()

    authors = populate_authors(n=2)
    session.add_all(authors)
    db_book.authors = authors
    session.commit()

    assert User.query.get(user_id) is not None, "User does not exist"
    assert (
        RentalLog.query.filter_by(user_id=user_id).count() == 1
    ), "RentalLog add failed"
    assert (
        Copy.query.filter_by(library_item=db_book).count() == 1
    ), "Copy add failed"

    book_one = (
        Book.query.join(Author.books).filter(Author.id == authors[0].id).all()
    )
    book_two = (
        Book.query.join(Author.books).filter(Author.id == authors[1].id).all()
    )
    assert (
        book_two[0].id == book_one[0].id
    ), "Authors should write the same book"
    assert book_one[0].id == db_book.id, "Author does not point the right book"
    assert Book.query.get(db_book.id) is not None, "Book does not exist"

    session.delete(db_book)
    session.commit()

    assert Book.query.get(db_book.id) is None, "Book delete failed"
    assert (
        User.query.get(user_id) is not None
    ), "User was deleted with the Book"
    assert (
        Copy.query.get(copy.id) is None
    ), "Copy was not deleted with the Book"

    assert (
        Book.query.join(
            Author.books
        ).filter(
            Author.id == authors[0].id
        ).all() == []
    ), "Author 0 should not contain the Book"
    assert (
        Book.query.join(
            Author.books
        ).filter(
            Author.id == authors[1].id
        ).all() == []
    ), "Author 1 should not contain the Book"
    assert (
        RentalLog.query.get(log.id) is None
    ), "RentalLog was not deleted with the Book"


def test_delete_authors(session, db_book):
    authors = populate_authors(2)
    session.add_all(authors)
    session.commit()
    db_book.authors = authors
    session.commit()

    assert (
        Book.query.join(
            Author.books
        ).filter(
            Book.id == db_book.id
        ).count() == 2
    ), "The book should have two authors"

    session.delete(authors[0])
    session.commit()
    assert (
        Book.query.join(
            Author.books
        ).filter(
            Book.id == db_book.id
        ).count() == 1
    ), "The book should have one author"

    session.delete(authors[1])
    session.commit()
    assert (
        Book.query.join(
            Author.books
        ).filter(
            Book.id == db_book.id
        ).count() == 0
    ), "The book should have zero authors"


def test_delete_copy(session, db_user, db_book):
    g = Generic("en")
    user_id = db_user.id
    copy = Copy(
        asset_code="{}{}".format(
            g.code.locale_code()[:2], g.code.pin(mask="######")
        ),
        library_item=db_book,
        shelf=g.code.pin(),
        has_cd_disk=g.development.boolean(),
    )
    session.add(copy)
    session.commit()
    log = RentalLog(
        copy_id=copy.id,
        user_id=user_id,
        borrow_time=datetime.now(tz=pytz.utc),
        return_time=datetime.now(tz=pytz.utc),
        book_status=BookStatus.BORROWED,
    )
    session.add(log)
    session.commit()

    assert User.query.get(user_id) is not None, "User does not exist"
    assert (
        RentalLog.query.filter_by(user_id=user_id).count() == 1
    ), "RentalLog add failed"
    assert (
        Copy.query.filter_by(library_item=db_book).count() == 1
    ), "Copy add failed"
    assert Book.query.get(db_book.id) is not None, "Book does not exist"

    session.delete(copy)
    session.commit()

    assert Copy.query.get(copy.id) is None, "Copy delete failed"
    assert (
        Book.query.get(db_book.id) is not None
    ), "Book was deleted with the Copy"
    assert (
        User.query.get(user_id) is not None
    ), "User was deleted with the Copy"
    assert (
        RentalLog.query.get(log.id) is None
    ), "RentalLog was not deleted with the Copy"
