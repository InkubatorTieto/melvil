from enum import Enum
from sqlalchemy import Table, Column, Integer, String, Boolean, \
    MetaData, ForeignKey, DateTime, create_engine
from sqlalchemy.engine import Connection
from sqlalchemy_utils import ChoiceType


class BookStatus(Enum):
    RESERVED = 1
    BORROWED = 2
    RETURNED = 3


class DataAccessLayer:
    connection = None
    metadata = None
    engine = None
    copy = None
    rental_log = None
    users = None

    def __init__(self, *args):
        self.metadata = MetaData()

        self.users = Table('users',
                           self.metadata,
                           Column('id', Integer, primary_key=True),
                           Column('email', String(128)),
                           Column('first_name', String(64)),
                           Column('surname', String(64)))

        self.copy = Table('copy',
                          self.metadata,
                          Column('id', Integer, primary_key=True),
                          Column('asset_code', String, unique=True),
                          Column('library_item_id', Integer),
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
                                Column('users_id',
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
