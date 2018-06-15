from flask import url_for


def test_dashboard_status_code(session, client):
    resp = client.get(url_for('library.book_borrowing_dashboad'))
    assert resp.status_code == 200
