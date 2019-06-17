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
    engine = None
    connection_string = None
    metadata = MetaData()

    copy = Table('copy', metadata,
        Column('id', Integer, primary_key=True),
        Column('asset_code', String, unique=True),
        Column('library_item_id', Integer),
        Column('shelf', String),
        Column('has_cd_disk', Boolean),
        Column('available_status', ChoiceType(BookStatus, impl=Integer())))

    rental_log = Table('rental_log', metadata,
        Column('id', Integer, primary_key=True),
        Column('copy_id', Integer, ForeignKey("copy.id"), nullable=False),
        Column('_borrow_time', DateTime),
        Column('_return_time', DateTime),
        Column('book_status', ChoiceType(BookStatus, impl=Integer())),
        Column('_reservation_begin', DateTime),
        Column('_reservation_end', DateTime))

    def init(self, connection_string):
        self.connection_string = connection_string
        self.engine = create_engine(connection_string)
        self.connection = Connection(self.engine)

data_access_layer = DataAccessLayer()
