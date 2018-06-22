from init_db import ma
from models.wishlist import WishListItem


class WishListItemSchema(ma.ModelSchema):
    class Meta:
        model = WishListItem
