from sqlalchemy import func

import flask
from flask import url_for

from models.users import RoleEnum, Role
from models.library import LibraryItem


def test_search_get(client, app_session):
    resp = client.get(url_for('library.search'))
    assert resp.status_code == 200,\
        "Client got wrong HTTP response!"


def test_search_post(client, app_session):
    resp = client.post(url_for('library.search'))
    assert resp.status_code == 405,\
        "Client got wrong HTTP response!"


def test_has_role(client, db_user):
    role_admin = Role.query.filter_by(name=RoleEnum.ADMIN).first()
    db_user.roles.append(role_admin)
    assert db_user.has_role('ADMIN'), \
        "User does not have admin privileges!"


def test_search_queries(app_session, search_query):
    query_all = LibraryItem.query.all()
    assert len(query_all) == 40, \
        "Query number not match with objects' number in db!"


def test_search_queries_sorted(app_session):
    query_all = LibraryItem.query.order_by(LibraryItem.title).all()
    assert all(
        query_all[i].title.lower() <= query_all[i + 1].title.lower()
        for i in range(len(query_all) - 1)), \
        "Items are not sorted by their title!"


def test_search_any(app_session, search_form):
    lib_items = LibraryItem.query.filter(
        func.lower(LibraryItem.title).like("%{}%".format(search_form.data)))
    if not lib_items:
        assert False, "There are items with such word"
    if lib_items:
        assert True, "There are no such items in library"


def test_search_query(app_session, get_title):
    lib_items = LibraryItem.query.filter(
        func.lower(LibraryItem.title).like("%{}%".format(get_title.title)))

    if lib_items:
        for item in lib_items:
            assert item.type == 'book' or item.type == 'magazine', \
                'Wrong objects queried!'
            assert get_title.title in item.title, \
                'Search query does not match title of item!'


def test_search_pagination(app):
    with app.test_request_context(f"/search?page="):
        assert flask.request.path == '/search'
        assert flask.request.args['page'] == ''
        page = 1
        paginate_query = LibraryItem.query.order_by(
            LibraryItem.title.asc()).paginate(page,
                                              error_out=True,
                                              max_per_page=10)
        assert paginate_query.total == 40
        assert len(paginate_query.items) <= 10

        for i in range(1, paginate_query.pages):

            with app.test_request_context(f"search?page={i}"):
                assert flask.request.path == '/search'
                assert flask.request.args['page'] == f'{i}'
                paginate_query = LibraryItem.query.order_by(
                    LibraryItem.title.asc()).paginate(page,
                                                      error_out=True,
                                                      max_per_page=10)
                assert paginate_query.total == 40
                assert len(paginate_query.items) <= 10

                if i == 1:
                    assert not paginate_query.has_prev
                    assert paginate_query.has_next
                if i == paginate_query.pages:
                    assert paginate_query.has_prev
                    assert not paginate_query.has_next


def test_search_serializer(app):
    with app.test_request_context(f"/search?page="):
        assert flask.request.path == '/search'
        assert flask.request.args['page'] == ''
        page = 1
        paginate_query = LibraryItem.query.order_by(
            LibraryItem.title.asc()).paginate(page,
                                              error_out=True,
                                              max_per_page=10)
        output = [d.serialize() for d in paginate_query.items]
        assert len(output) == len(paginate_query.items)
