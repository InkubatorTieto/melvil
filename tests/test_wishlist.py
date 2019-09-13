import datetime as d
from datetime import datetime

import flask
import pytest
from flask import url_for
from sqlalchemy import func

from models import Like, WishListItem


def test_add_wishlist_item_from_view(client, view_wish_list):
    resp = client.post(url_for('library.add_wish'),
                       data=view_wish_list.data,
                       follow_redirects=True)
    assert resp.status_code == 200
    assert WishListItem.query\
        .filter_by(authors=view_wish_list.authors.data)\
        .scalar is not None


@pytest.mark.parametrize("values, result", [
    ("1899", False),
    ("1999", True),
    ("2000", True),
    ((datetime.today().date() + d.timedelta(days=1)).year, False)
])
def test_check_pub_date(view_wish_list, values, result):
    view_wish_list.pub_date.data = values
    view_wish_list.pub_date.validate(view_wish_list)
    assert bool(view_wish_list.errors) != result, \
        "The validator 'check_pub_date' returns not" \
        " a valid value\n Errors:{0}".format(view_wish_list.errors)


def test_add_like_function(db_user, db_wishlist_item):
    Like.like(db_wishlist_item.id, db_user)
    assert Like.like_exists(db_wishlist_item.id, db_user)
    Like.unlike(db_wishlist_item.id, db_user)
    assert not Like.like_exists(db_wishlist_item.id, db_user)


def test_wish_delete(db_wishlist_item):
    db_wishlist_item.delete_wish(db_wishlist_item.id)
    assert WishListItem.query.filter_by(
        id=db_wishlist_item.id)\
        .scalar() is None, "Wish delete failed"


def test_wish_queries(app_session, wishlist_query):
    query_all = WishListItem.query.all()
    assert len(query_all) == 30, \
        "Query number not match with objects' number in db!"


def test_wish_any(app_session, search_form):
    wish_items = WishListItem.query.filter(
        func.lower(WishListItem.title).like("%{}%".format(search_form.data)))
    if not wish_items:
        assert False, "There are wishes with such word"
    if wish_items:
        assert True, "There are no such wishes in db_user"


def test_wish_query(app_session, get_wish):
    wish_items = WishListItem.query.filter(
        func.lower(WishListItem.title).like("%{}%".format(get_wish.title)))

    if wish_items:
        for wish in wish_items:
            assert wish.type == 'book' or wish.type == 'magazine', \
                'Wrong objects queried!'
            assert get_wish.title in wish.title, \
                'Search query does not match title of item!'


def test_wish_pagination(app):
    with app.test_request_context(f"/wishlist?page="):
        assert flask.request.path == '/wishlist'
        assert flask.request.args['page'] == ''
        page = 1
        paginate_query = WishListItem.query.order_by(
            WishListItem.likes_count.desc()).order_by(
            WishListItem.title.asc()).paginate(page,
                                               error_out=True,
                                               max_per_page=5)
        assert paginate_query.total == 30
        assert len(paginate_query.items) <= 5

        for i in range(1, paginate_query.pages):

            with app.test_request_context(f"wishlist?page={i}"):
                assert flask.request.path == '/wishlist'
                assert flask.request.args['page'] == f'{i}'
                paginate_query = WishListItem.query.order_by(
                    WishListItem.likes_count.desc()).order_by(
                    WishListItem.title.asc()).paginate(page,
                                                       error_out=True,
                                                       max_per_page=5)
                assert paginate_query.total == 30
                assert len(paginate_query.items) <= 5

                if i == 1:
                    assert not paginate_query.has_prev
                    assert paginate_query.has_next
                if i == paginate_query.pages:
                    assert paginate_query.has_prev
                    assert not paginate_query.has_next


def test_wish_serializer(app):
    with app.test_request_context(f"/search?page="):
        assert flask.request.path == '/search'
        assert flask.request.args['page'] == ''
        page = 1
        paginate_query = WishListItem.query.order_by(
            WishListItem.likes_count.desc()).order_by(
            WishListItem.title.asc()).paginate(page,
                                               error_out=True,
                                               max_per_page=5)
        output = [d.serialize() for d in paginate_query.items]
        assert len(output) == len(paginate_query.items)

        for wish, item in zip(output, paginate_query.items):
            assert wish['id'] == item.id
            assert wish['item_type'] == item.item_type
            assert wish['title'] == item.title
            assert wish['authors'] == item.authors
            assert wish['pub_year'] == item.pub_year
            assert wish['likes'] == item.likes
