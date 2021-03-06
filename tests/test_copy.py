import re
from unittest import mock

import pytest
from flask import url_for, session

from models import Copy


def check_copy_properties(copy_form, db_book, copy, copy_before_edit=None):
    index = 0
    if copy_before_edit:
        index = 1
        assert copy.id == copy_before_edit.id, \
            "Edited copy does not replace old version of copy"
    assert copy, \
        "Copy not added to db"
    assert copy.library_item_id == db_book.id, \
        "Added copy pointed wrong book id"
    assert copy.library_item == db_book, \
        "Added copy pointed wrong book"
    assert copy.available_status, \
        "Added copy has wrong available status"
    assert copy.has_cd_disk, \
        "Added copy has wrong has_cd_disk status"
    assert copy.asset_code == copy_form[index].asset_code.data, \
        "Added copy asset_code is not the one from the Form"
    assert copy.shelf == copy_form[index].shelf.data, \
        "Added copy shelf is not the one from the Form"
    session.clear()


def test_add_get_status_code(
    client,
    db_book,
    login_form_admin_credentials,
    mock_ldap
):
    with mock.patch('views.index.ldap_client', mock_ldap):
        client.post(url_for('library.login'),
                    data=login_form_admin_credentials.data)
        resp = client.get(url_for('library.add_copy', item_id=db_book.id))
        assert resp.status_code == 200, \
            "Add_copy GET view wrong response"
        session.clear()


def test_add_post_nothing_status_code(client, db_book):
    resp = client.post(url_for('library.add_copy',
                               item_id=db_book.id))
    assert resp.status_code == 302, \
        "Add_copy POST view wrong response"


def test_add_post_data_status_code(copy_form, client, db_book):
    resp = client.post(url_for('library.add_copy',
                               item_id=db_book.id),
                       data=copy_form[0].data)
    assert resp.status_code == 302, \
        "Add_copy POST crashed redirect"


def test_add_post_data_redirect_status_code(
        copy_form,
        client,
        db_book,
        app_session):
    resp = client.post(url_for('library.add_copy', item_id=db_book.id),
                       data=copy_form[0].data, follow_redirects=True)
    assert resp.status_code == 200, \
        "Item_description view redirected from Add_copy view wrong response"


def test_db_after_add_copy(
    copy_form,
    db_book,
    client,
    login_form_admin_credentials,
    mock_ldap
):
    with mock.patch('views.index.ldap_client', mock_ldap):
        client.post(url_for('library.login'),
                    data=login_form_admin_credentials.data)
        client.post(url_for('library.add_copy',
                            item_id=db_book.id),
                    data=copy_form[0].data)
        copy = Copy.query.filter_by(
            asset_code=copy_form[0].asset_code.data).first()
        check_copy_properties(copy_form, db_book, copy)
        session.clear()


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
                .match(values)) == expected, \
        "Regex for asset code is wrong"


def test_edit_get_status_code(
    client,
    db_copies,
    login_form_admin_credentials,
    mock_ldap
):
    with mock.patch('views.index.ldap_client', mock_ldap):
        resp = client.post(
            url_for('library.login'),
            data=login_form_admin_credentials.data
        )
        assert resp.status_code == 200, \
            "Edit_copy GET view wrong response"
        resp = client.get(url_for(
            'library.edit_copy',
            copy_id=db_copies[0].id
        ))
        assert resp.status_code == 200, \
            "Edit_copy GET view wrong response"
        session.clear()


def test_edit_post_nothing_status_code(client, db_copies):
    resp = client.post(url_for('library.edit_copy',
                               copy_id=db_copies[0].id))
    assert resp.status_code == 302, \
        "Edit_copy POST view wrong response"


def test_edit_post_data_status_code(copy_form, client, db_copies):
    resp = client.post(url_for('library.edit_copy',
                               copy_id=db_copies[0].id),
                       data=copy_form[1].data)
    assert resp.status_code == 302, \
        "Edit_copy POST crashed redirect"


def test_edit_post_data_redirect_status_code(
        copy_form,
        client,
        db_copies,
        app_session):
    resp = client.post(url_for('library.edit_copy', copy_id=db_copies[0].id),
                       data=copy_form[1].data, follow_redirects=True)
    assert resp.status_code == 200, \
        "Item_description view redirected from Edit_copy view wrong response"


def test_db_after_edit_copy(
    copy_form,
    db_copies,
    client,
    db_book,
    login_form_admin_credentials,
    mock_ldap
):
    with mock.patch('views.index.ldap_client', mock_ldap):
        client.post(url_for('library.login'),
                    data=login_form_admin_credentials.data)
        client.post(url_for('library.add_copy',
                            item_id=db_book.id), data=copy_form[0].data)
        copy_before_edit = Copy.query.get(db_copies[0].id)
        client.post(url_for('library.edit_copy',
                            copy_id=db_copies[0].id),
                    data=copy_form[1].data)
        copy = Copy.query.get(db_copies[0].id)
        check_copy_properties(copy_form, db_book, copy, copy_before_edit)
        session.clear()
