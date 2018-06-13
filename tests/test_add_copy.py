from flask import url_for

from models import Copy


def test_get_status_code(client, db_book):
    resp = client.get(url_for('library.add_copy',
                              item_id=db_book.id))
    assert resp.status_code == 200


def test_post_nothing_status_code(client, db_book):
    resp = client.post(url_for('library.add_copy',
                               item_id=db_book.id))
    assert resp.status_code == 200


def test_post_data_status_code(copy_form, client, db_book):
    resp = client.post(url_for('library.add_copy',
                               item_id=db_book.id),
                       data=copy_form.data)
    assert resp.status_code == 302


def test_post_data_redirect_status_code(
        copy_form,
        client,
        db_book,
        app_session):
    resp = client.post(url_for('library.add_copy', item_id=db_book.id),
                       data=copy_form.data, follow_redirects=True)
    assert resp.status_code == 200


def test_db_after_add_copy(copy_form, db_book, client):
    client.post(url_for('library.add_copy',
                        item_id=db_book.id),
                data=copy_form.data)

    copy = Copy.query.filter_by(asset_code=copy_form.asset_code.data).first()
    assert copy
    assert copy.library_item_id == db_book.id
    assert copy.library_item == db_book
    assert copy.available_status

    assert copy.asset_code == copy_form.asset_code.data
    assert copy.shelf == copy_form.shelf.data
