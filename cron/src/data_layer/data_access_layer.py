from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer,
                        MetaData, String, Table, create_engine)
from sqlalchemy.engine import Connection
from sqlalchemy_utils import ChoiceType

from .book_status import BookStatus


class DataAccessLayer:
    connection = None
    metadata = None
    engine = None
    library_item = None
    copy = None
    rental_log = None
    users = None

    def __init__(self, *args):
        self.metadata = MetaData()

        self.library_item = Table('library_item',
                                  self.metadata,
                                  Column('id', Integer, primary_key=True),
                                  Column('title', String(256)))

        self.users = Table('users',
                           self.metadata,
                           Column('id', Integer, primary_key=True),
                           Column('email', String(128)),
                           Column('first_name', String(64)),
                           Column('surname', String(64)),
                           Column('employee_id', String(64)))

        self.copy = Table('copy',
                          self.metadata,
                          Column('id', Integer, primary_key=True),
                          Column('asset_code', String, unique=True),
                          Column('library_item_id',
                                 Integer,
                                 ForeignKey("library_item.id"),
                                 nullable=False),
                          Column('shelf', String),
                          Column('has_cd_disk', Boolean),
                          Column('available_status',
                                 ChoiceType(BookStatus, impl=Integer())))

        self.rental_log = Table('rental_log',
                                self.metadata,
                                Column('id', Integer, primary_key=True),
                                Column('copy_id',
                                       Integer,
                                       ForeignKey("copy.id"),
                                       nullable=False),
                                Column('user_id',
                                       Integer,
                                       ForeignKey("users.id"),
                                       nullable=False),
                                Column('_borrow_time', DateTime),
                                Column('_return_time', DateTime),
                                Column('book_status',
                                       ChoiceType(BookStatus, impl=Integer())),
                                Column('_reservation_begin', DateTime),
                                Column('_reservation_end', DateTime))

        self.engine = create_engine(*args)
        self.connection = Connection(self.engine)
