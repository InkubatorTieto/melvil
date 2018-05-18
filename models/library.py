from app import db


class RentalLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_copy_id = db.Column(db.Integer,
                             db.ForeignKey('copy.id'))
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))
    borrow_time = db.Column(db.DateTime)
    return_time = db.Column(db.DateTime)
    returned = db.Column(db.Boolean)

    def __repr__(self):
        return "User ID: {} - Book ID: {}".\
            format(self.user_id, self.book_copy_id)
