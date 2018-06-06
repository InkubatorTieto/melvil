from init_db import db, ma


class Like(db.Model):
    __tablename__ = 'wish_list_likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    wish_item_id = db.Column(db.Integer, db.ForeignKey('wish_list_items.id'), nullable=False)

    def __repr__(self):
        return '<Like {}>'.format(self.wish_item_id, self.user_id)


class LikeSchema(ma.ModelSchema):
    class Meta:
        model = Like


class WishListItem(db.Model):
    __tablename__ = 'wish_list_items'
    id = db.Column(db.Integer, primary_key=True)
    authors = db.Column(db.String(256))
    title = db.Column(db.String(256))
    likes = db.relationship('Like', backref='wish_list_item',  cascade="all, delete-orphan", lazy=True)
    pub_year = db.Column(db.Date)

    def __repr__(self):
        return '<Wish List Item {}>'.format(self.likes)


class WishListItemSchema(ma.ModelSchema):
    class Meta:
        model = WishListItem





