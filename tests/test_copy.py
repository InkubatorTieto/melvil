import re

import pytest
from flask import url_for

from models import Copy


def test_add_get_status_code(client, db_book):
    resp = client.get(url_for('library.add_copy',
                              item_id=db_book.id))
    assert resp.status_code == 200


def test_add_post_nothing_status_code(client, db_book):
    resp = client.post(url_for('library.add_copy',
                               item_id=db_book.id))
    assert resp.status_code == 200


def test_add_post_data_status_code(copy_form, client, db_book):
    resp = client.post(url_for('library.add_copy',
                               item_id=db_book.id),
                       data=copy_form[0].data)
    assert resp.status_code == 302


def test_add_post_data_redirect_status_code(
        copy_form,
        client,
        db_book,
        app_session):
    resp = client.post(url_for('library.add_copy', item_id=db_book.id),
                       data=copy_form[0].data, follow_redirects=True)
    assert resp.status_code == 200


def test_db_after_add_copy(copy_form, db_book, client):
    client.post(url_for('library.add_copy',
                        item_id=db_book.id),
                data=copy_form[0].data)

    copy = Copy.query.filter_by(
        asset_code=copy_form[0].asset_code.data).first()
    assert copy
    assert copy.library_item_id == db_book.id
    assert copy.library_item == db_book
    assert copy.available_status
    assert copy.has_cd_disk
    assert copy.asset_code == copy_form[0].asset_code.data
    assert copy.shelf == copy_form[0].shelf.data


@pytest.mark.parametrize("values, expected", [
    ("WR010203", True),
    ("wr010203", True),
    ("aB123456", True),
    ("abc", False),
    ("abc12345", False),
    (".", False),
    ("12345678", False),
    ("abcdeFgH", False),
])
def test_asset_code_regex(values, expected):
    assert bool(re.compile('^[A-Z]{2}[0-9]{6}$', flags=re.IGNORECASE)
                .match(values)) == expected


def test_edit_get_status_code(client, db_copies):
    resp = client.get(url_for('library.edit_copy',
                              copy_id=db_copies[0].id))
    assert resp.status_code == 200


def test_edit_post_nothing_status_code(client, db_copies):
    resp = client.post(url_for('library.edit_copy',
                               copy_id=db_copies[0].id))
    assert resp.status_code == 200


def test_edit_post_data_status_code(copy_form, client, db_copies):
    resp = client.post(url_for('library.edit_copy',
                               copy_id=db_copies[0].id),
                       data=copy_form[1].data)
    assert resp.status_code == 302


def test_edit_post_data_redirect_status_code(
        copy_form,
        client,
        db_copies,
        app_session):
    resp = client.post(url_for('library.edit_copy', copy_id=db_copies[0].id),
                       data=copy_form[1].data, follow_redirects=True)
    assert resp.status_code == 200


def test_db_after_edit_copy(copy_form, db_copies, client, db_book):
    client.post(url_for('library.add_copy',
                        item_id=db_book.id),
                data=copy_form[0].data)
    copy_before_edit = Copy.query.get(db_copies[0].id)

    client.post(url_for('library.edit_copy',
                        copy_id=db_copies[0].id),
                data=copy_form[1].data)
    copy = Copy.query.get(db_copies[0].id)

    assert copy
    assert copy.id == copy_before_edit.id
    assert copy.library_item_id == db_book.id
    assert copy.library_item == db_book
    assert copy.available_status
    assert copy.has_cd_disk
    assert copy.asset_code == copy_form[1].asset_code.data
    assert copy.shelf == copy_form[1].shelf.data
