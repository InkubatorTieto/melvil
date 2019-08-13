from data_layer.data_access_layer import DataAccessLayer
from data_layer.book_status import BookStatus
from datetime import datetime
import pytest


def prepare_db(dal):
    connection = dal.connection
    library_item = dal.library_item
    copy = dal.copy
    rental_log = dal.rental_log
    users = dal.users

    connection.execute(
        library_item.insert(), [
            {
                'id': 1,
                'title': 'Very interesing book'
            },
            {
                'id': 2,
                'title': 'The book part 2'
            },
        ]
    )

    connection.execute(
        users.insert(), [
            {
                'id': 1,
                'employee_id': '1',
                'email': 'id_1@example.com',
                'first_name': 'id_1_first_name',
                'surname': 'id_1_surname'
            },
            {
                'id': 2,
                'employee_id': '2',
                'email': 'id_2@example.com',
                'first_name': 'id_2_first_name',
                'surname': 'id_2_surname'
            }
        ]
    )

    connection.execute(
        copy.insert(), [
            {
                'id': 1,
                'asset_code': '1',
                'library_item_id': 1,
                'shelf': 'None',
                'has_cd_disk': False,
                'available_status': BookStatus.BORROWED
            },
            {
                'id': 2,
                'asset_code': '2',
                'library_item_id': 1,
                'shelf': 'None',
                'has_cd_disk': False,
                'available_status': BookStatus.RESERVED
            },
            {
                'id': 3,
                'asset_code': '3',
                'library_item_id': 1,
                'shelf': 'None',
                'has_cd_disk': False,
                'available_status': BookStatus.RESERVED
            },
            {
                'id': 4,
                'asset_code': '4',
                'library_item_id': 1,
                'shelf': 'None',
                'has_cd_disk': False,
                'available_status': BookStatus.RESERVED
            },
            {
                'id': 5,
                'asset_code': '5',
                'library_item_id': 2,
                'shelf': 'None',
                'has_cd_disk': False,
                'available_status': BookStatus.BORROWED
            },
            {
                'id': 6,
                'asset_code': '6',
                'library_item_id': 2,
                'shelf': 'None',
                'has_cd_disk': False,
                'available_status': BookStatus.BORROWED
            }
        ])

    connection.execute(
        rental_log.insert(), [
            {
                'id': 1,
                'copy_id': 2,
                'user_id': 1,
                'book_status': BookStatus.RESERVED,
                '_reservation_end': datetime(2030, 5, 4),
                '_return_time': None
            },
            {
                'id': 2,
                'copy_id': 3,
                'user_id': 1,
                'book_status': BookStatus.RESERVED,
                '_reservation_end': datetime(2030, 5, 5),
                '_return_time': None
            },
            {
                'id': 3,
                'copy_id': 4,
                'user_id': 1,
                'book_status': BookStatus.RESERVED,
                '_reservation_end': datetime(2030, 5, 7),
                '_return_time': None
            },
            {
                'id': 4,
                'copy_id': 1,
                'user_id': 1,
                'book_status': BookStatus.BORROWED,
                '_reservation_end': datetime(2030, 5, 7),
                '_return_time': datetime(2030, 5, 7)
            },
            {
                'id': 5,
                'copy_id': 5,
                'user_id': 1,
                'book_status': BookStatus.BORROWED,
                '_reservation_end': datetime(2030, 5, 7),
                '_return_time': datetime(2030, 5, 7)
            },
            {
                'id': 6,
                'copy_id': 6,
                'user_id': 2,
                'book_status': BookStatus.BORROWED,
                '_reservation_end': datetime(2030, 5, 7),
                '_return_time': datetime(2030, 5, 7)
            }
        ]
    )


@pytest.fixture()
def data_access_layer():
    dal = DataAccessLayer('sqlite:///:memory:')
    dal.metadata.create_all(dal.engine)
    prepare_db(dal)

    def func(*args, **kwargs):
        return dal.connection

    dal.connection.execution_options = func
    return dal
