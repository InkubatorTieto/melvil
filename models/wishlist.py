from init_db import db


class WishListItem(db.Model):
   __tablename__ = 'wish_list_items'
   id = db.Column(db.Integer, primary_key=True)
   authors = db.Column(db.String(256))
   title = db.Column(db.String(256))
  # likes = db.Column(db.Integer)
   pub_date = db.Column(db.Date)

   def __repr__(self):
       return '{0}. {1} {2} {3}'.format((self.id),(self.authors),(self.title),(self.pub_date))


# class Like(db.Model):
#    __tablename__ = 'wish_list_likes'
#    id = db.Column(db.Integer)
#    user_id = db.Column(db.Integer,
#                        db.ForeignKey('users.id'),
#                        nullable=False)
#    wish_item_id = db.Column(db.Integer,
#                             db.ForeignKey('wish_list_items'),
#                             nullable=False)
#    like = db.Column(db.Boolean)
#
#    def __repr__(self):
#        return '<Wish List Item {}>'.format(self.like)