from sqlalchemy import func

from flask import url_for

from models.users import RoleEnum, Role
from models.library import LibraryItem


def test_search_get(client, app_session):
    resp = client.get(url_for('library.search'))
    assert resp.status_code == 200


def test_has_role(db_user):
    role_admin = Role.query.filter_by(name=RoleEnum.ADMIN).first()
    db_user.roles.append(role_admin)
    assert db_user.has_role('ADMIN'), \
        "has_role() method on User model does not work properly"


def test_search_query_match(client, app_session, search_query):
    query_all = LibraryItem.query.all()
    assert len(query_all) == 40


def test_search_query_null(client, app_session, search_form):
    resp = client.get(url_for('library.search'),
                       data=search_form.data,
                       follow_redirects=True)
    assert resp.status_code == 200

    lib_items = LibraryItem.query.filter(
        func.lower(LibraryItem.title).like("%{}%".format(search_form.data)))

    if not lib_items:
        assert False, "There are items with such word"
    if lib_items:
        assert True, "There are no such items in library"


def test_search_query(client, app_session, get_title):
    resp = client.get(url_for('library.search'),
                       data=get_title.title,
                       follow_redirects=True)
    assert resp.status_code == 200

    lib_items = LibraryItem.query.filter(
        func.lower(LibraryItem.title).like("%{}%".format(get_title.title)))

    if lib_items:
        for item in lib_items:
            assert item.type == 'book' or item.type == 'magazine', \
                'Wrong objects queried!'
            assert get_title.title in item.title, \
                'Search query does not match title of item!'
