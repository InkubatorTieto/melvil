from flask import url_for
from views.book_borrowing_dashboard import (
    get_reserved_items,
    get_borrowed_items,
)


def test_dashboard_status_code(client):
    resp = client.get(url_for(
        'library_book_borrowing_dashboard.book_borrowing_dashboad'))
    assert resp.status_code == 200


def test_get_reserved_items(session, user_reservations):
    reserved_items = get_reserved_items(session, user_reservations[0].id)
    assert reserved_items[0].LibraryItem == user_reservations[1][0]
    assert reserved_items[0]._reservation_begin == \
        user_reservations[1][1]._reservation_begin
    assert reserved_items[0]._reservation_end == \
        user_reservations[1][1]._reservation_end
    assert reserved_items[1].LibraryItem == user_reservations[3][0]
    assert reserved_items[1]._reservation_begin == \
        user_reservations[3][1]._reservation_begin
    assert reserved_items[1]._reservation_end == \
        user_reservations[3][1]._reservation_end


def test_get_borrowed_items(session, user_reservations):
    borrowed_items = get_borrowed_items(session, user_reservations[0].id)
    assert borrowed_items[0].LibraryItem == \
        user_reservations[4][0]
    assert borrowed_items[0]._borrow_time == \
        user_reservations[4][1]._borrow_time
    assert borrowed_items[0]._return_time == \
        user_reservations[4][1]._return_time
    assert borrowed_items[1].LibraryItem == user_reservations[2][0]
    assert borrowed_items[1]._borrow_time == \
        user_reservations[2][1]._borrow_time
    assert borrowed_items[1]._return_time == \
        user_reservations[2][1]._return_time
