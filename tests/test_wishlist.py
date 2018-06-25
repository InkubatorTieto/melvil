from flask import url_for
import pytest
import datetime as d
from datetime import datetime


from models import (WishListItem, Like)


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
