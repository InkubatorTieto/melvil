from models import WishListItem


def test_wish_delete(db_wishlist_item):
    db_wishlist_item.deleteWish(db_wishlist_item.id)
    assert WishListItem.query.filter_by(
        id=db_wishlist_item.id)\
        .scalar() is None, "Wish delete failed"
