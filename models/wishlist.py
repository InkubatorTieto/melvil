from init_db import db


class Like(db.Model):
    __tablename__ = 'wish_list_likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    wish_item_id = db.Column(db.Integer,
                             db.ForeignKey('wish_list_items.id'),
                             nullable=False)

    def __repr__(self):
        return '<Like {}>'.format(self.id,)

    @classmethod
    def like_exists(cls, wish_id, user):
        return db.session.query(Like.id)\
                 .filter_by(user_id=user.id, wish_item_id=wish_id)\
                 .scalar() is not None

    @classmethod
    def like(cls, wish_id, user):
        new_like = Like(user_id=user.id, wish_item_id=wish_id)
        db.session.add(new_like)
        db.session.commit()

    @classmethod
    def unlike(cls, wish_id, user):
        unlike = Like.query\
            .filter_by(user_id=user.id, wish_item_id=wish_id).first()
        db.session.delete(unlike)
        db.session.commit()


class WishListItem(db.Model):
    __tablename__ = 'wish_list_items'
    id = db.Column(db.Integer, primary_key=True)
    authors = db.Column(db.String(256))
    title = db.Column(db.String(256), nullable=False)
    likes = db.relationship('Like',
                            backref='wish_list_item',
                            cascade="all, delete-orphan",
                            lazy=True)
    pub_year = db.Column(db.Date)
    item_type = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return '<Wish List Item {}>'.format(self.title)

    @classmethod
    def delete_wish(cls, wish_id):
        delete_wish_admin = WishListItem.query.get(wish_id)
        db.session.delete(delete_wish_admin)
        db.session.commit()
