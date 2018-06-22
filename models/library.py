from enum import Enum
import pytz
from sqlalchemy_utils import ChoiceType
from init_db import db


class Copy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_code = db.Column(db.String(8), unique=True)
    library_item_id = db.Column(db.Integer,
                                db.ForeignKey('library_item.id'),
                                nullable=False)
    library_item = db.relationship('LibraryItem',
                                   foreign_keys=library_item_id,
                                   uselist=False,
                                   backref=db.backref(
                                       'copies',
                                       lazy='select',
                                       cascade='all, delete-orphan'))
    shelf = db.Column(db.String(56))
    has_cd_disk = db.Column(db.Boolean)
    available_status = db.Column(db.Boolean, server_default='t', default=True)
    rental_logs = db.relationship('RentalLog',
                                  lazy='dynamic',
                                  cascade='all, delete-orphan',
                                  backref=db.backref(
                                      'copy', uselist=False))

    def __str__(self):
        return "Copy asset_code: {}, type/title: {}/{}".format(
            self.asset_code,
            self.library_item.type,
            self.library_item.title
        )

    def __repr__(self):
        return "<Copy: {} library_item_id={}>".format(
            self.asset_code,
            self.library_item_id
        )


class BookStatus(Enum):
    RESERVED = 1
    BORROWED = 2
    RETURNED = 3


class RentalLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    copy_id = db.Column(db.Integer,
                        db.ForeignKey('copy.id'),
                        nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)
    _borrow_time = db.Column(db.DateTime)
    _return_time = db.Column(db.DateTime)
    book_status = db.Column(ChoiceType(BookStatus, impl=db.Integer()))
    _reservation_begin = db.Column(db.DateTime)
    _reservation_end = db.Column(db.DateTime)

    @property
    def borrow_time(self):
        return self._borrow_time.replace(tzinfo=pytz.utc).\
            astimezone(tz=pytz.timezone('Europe/Warsaw'))

    @borrow_time.setter
    def borrow_time(self, dt):
        if dt.tzinfo is None:
            raise ValueError("borrow_time has to be timezone aware")
        self._borrow_time = dt.astimezone(tz=pytz.utc)

    @property
    def return_time(self):
        return self._return_time.replace(tzinfo=pytz.utc). \
            astimezone(tz=pytz.timezone('Europe/Warsaw'))

    @return_time.setter
    def return_time(self, dt):
        if dt.tzinfo is None:
            raise ValueError("return_time has to be timezone aware")
        self._return_time = dt.astimezone(tz=pytz.utc)

    @property
    def reservation_begin(self):
        return self._reservation_begin.replace(tzinfo=pytz.utc). \
            astimezone(tz=pytz.timezone('Europe/Warsaw'))

    @reservation_begin.setter
    def reservation_begin(self, dt):
        if dt.tzinfo is None:
            raise ValueError("reservation_timestamp has to be timezone aware")
        self._reservation_begin = dt.astimezone(tz=pytz.utc)

    @property
    def reservation_end(self):
        return self._reservation_end.replace(tzinfo=pytz.utc). \
            astimezone(tz=pytz.timezone('Europe/Warsaw'))

    @reservation_end.setter
    def reservation_end(self, dt):
        if dt.tzinfo is None:
            raise ValueError("reservation_timestamp has to be timezone aware")
        self._reservation_end = dt.astimezone(tz=pytz.utc)

    def __str__(self):
        return "RENTAL LOG: user: {} copy: {}".format(
            self.user.full_name,
            self.copy.asset_code
        )

    def __repr__(self):
        return "<RentalLog: user_id={} copy_id={}>".format(
            self.user_id,
            self.copy_id
        )


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return "<Tag: {}>".format(self.name)

    def __str__(self):
        return "Tag: {}".format(self.name)


item_tags = db.Table('item_tags',
                     db.Column('item_id',
                               db.Integer,
                               db.ForeignKey('library_item.id')),
                     db.Column('tag_id',
                               db.Integer,
                               db.ForeignKey('tags.id')))


class LibraryItem(db.Model):
    __tablename__ = 'library_item'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    table_of_contents = db.Column(db.String(256))
    language = db.Column(db.String(56))
    category = db.Column(db.String(56))
    tags = db.relationship('Tag',
                           secondary=item_tags,
                           lazy='subquery',
                           backref=db.backref('library_items'))
    description = db.Column(db.Text)
    type = db.Column(db.String(32))

    __mapper_args__ = {
        'polymorphic_identity': 'library_item',
        'polymorphic_on': type
    }

    @property
    def tags_string(self):
        if self.tags:
            return ', '.join(t.name for t in self.tags)
        else:
            return '-'
