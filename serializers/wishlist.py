from init_db import ma
from models import WishListItem


class WishListItemSchema(ma.ModelSchema):
    class Meta:
        model = WishListItem