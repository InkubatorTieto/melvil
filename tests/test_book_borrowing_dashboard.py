from flask import url_for
from views.book_borrowing_dashboard import get_reserved_items
from flask import session
from tests.populate import (
    populate_users,
    populate_copies,
    populate_authors,
    populate_books,
    populate_rental_logs,
    populate_magazines
)
from models.library import BookStatus


def test_dashboard_status_code(client):
    resp = client.get(url_for('library_book_borrowing_dashboard.book_borrowing_dashboad'))
    assert resp.status_code == 200


def test_get_reserved_items(session):
    # user = populate_users(n=1)
    # session.add_all(user)
    # session.commit()
    # authors = populate_authors(n=2)
    # session.add_all(authors)
    # session.commit()
    # book1 = populate_books(n=1, authors=authors)
    # book2 = populate_books(n=1, authors=authors)
    # session.add_all(book1)
    # session.add_all(book2)
    # session.commit()
    # magazine1 = populate_magazines(n=1)
    # magazine2 = populate_magazines(n=1)
    # session.add_all(magazine1)
    # session.add_all(magazine2)
    # session.commit()
    # copy1 = populate_copies(book1[0], n=1)
    # copy2 = populate_copies(book2[0], n=1)
    # copy3 = populate_copies(magazine1[0], n=1)
    # copy4 = populate_copies(magazine2[0], n=1)
    # session.add_all(copy1)
    # session.add_all(copy2)
    # session.add_all(copy3)
    # session.add_all(copy4)
    # session.commit()
    # reservation1 = populate_rental_logs(copy1[0].id, user[0].id, n=1)
    # reservation2 = populate_rental_logs(copy2[0].id, user[0].id, n=1)
    # reservation3 = populate_rental_logs(copy3[0].id, user[0].id, n=1)
    # reservation4 = populate_rental_logs(copy4[0].id, user[0].id, n=1)
    # session.add_all(reservation1)
    # session.add_all(reservation2)
    # session.add_all(reservation3)
    # session.add_all(reservation4)
    # session.commit()
    # reservation1[0].book_status = BookStatus.RESERVED
    # reservation2[0].book_status = BookStatus.BORROWED
    # reservation3[0].book_status = BookStatus.RESERVED
    # reservation4[0].book_status = BookStatus.BORROWED

    reserved_items = get_reserved_items(session, user[0].id)
    assert len(reserved_items) == 2



