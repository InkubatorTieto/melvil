from flask import url_for, session
from views.book_borrowing_dashboard import (
    get_reserved_items,
    get_borrowed_items,
)


def test_check(mock_ldap):
    from app import ldap_client
    assert ldap_client.bind_user(ldap_client.user['user_name'], ldap_client.user['passwd'])


def test_dashboard_status_code(client, login_form_admin_credentials):
    client.post(url_for('library.login'),
                data=login_form_admin_credentials.data)
    resp = client.get(url_for(
        'library_book_borrowing_dashboard.book_borrowing_dashboad'))
    assert resp.status_code == 200
    session.clear()


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
