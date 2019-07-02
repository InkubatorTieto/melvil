from datetime import datetime
from freezegun import freeze_time

from data_access_layer import DataAccessLayer, BookStatus
from update_reservation_status import check_reservation_status_db
from sqlalchemy.sql import select
import pytest


def prepare_db(dal):
    connection = dal.connection
    copy = dal.copy
    rental_log = dal.rental_log

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
                'library_item_id': 2,
                'shelf': 'None',
                'has_cd_disk': False,
                'available_status': BookStatus.RESERVED
            },
            {
                'id': 3,
                'asset_code': '3',
                'library_item_id': 33,
                'shelf': 'None',
                'has_cd_disk': False,
                'available_status': BookStatus.RESERVED
            }
        ])

    connection.execute(
        rental_log.insert(), [
            {
                'id': 1,
                'copy_id': 2,
                'book_status': BookStatus.RESERVED,
                '_reservation_end': datetime(2030, 5, 5)
            },
            {
                'id': 33,
                'copy_id': 3,
                'book_status': BookStatus.RESERVED,
                '_reservation_end': datetime(2030, 5, 7)
            }
        ]
    )


@pytest.fixture
def data_access_layer():
    dal = DataAccessLayer('sqlite:///:memory:')
    dal.metadata.create_all(dal.engine)
    prepare_db(dal)

    def func(*args, **kwargs):
        return dal.connection

    dal.connection.execution_options = func
    return dal


@freeze_time(datetime(2030, 5, 6))
def test_clears_reservations_for_outdated_positions(data_access_layer):
    copy = data_access_layer.copy
    rental_log = data_access_layer.rental_log
    connection = data_access_layer.connection

    check_reservation_status_db(data_access_layer)

    copies = connection.execute(
        select([copy])
        .where(copy.c.available_status == BookStatus.RESERVED)
    ).fetchall()

    rentals = connection.execute(
        select([rental_log])
        .where(rental_log.c.book_status == BookStatus.RESERVED)
    ).fetchall()

    assert len(copies) == 1 and len(rentals) == 1


@freeze_time(datetime(2030, 5, 4))
def test_does_not_clear_valid_reservations(data_access_layer):
    copy = data_access_layer.copy
    rental_log = data_access_layer.rental_log
    connection = data_access_layer.connection

    check_reservation_status_db(data_access_layer)

    copies = connection.execute(
        select([copy])
        .where(copy.c.available_status == BookStatus.RESERVED)
    ).fetchall()

    rentals = connection.execute(
        select([rental_log])
        .where(rental_log.c.book_status == BookStatus.RESERVED)
    ).fetchall()

    assert len(copies) == 2 and len(rentals) == 2


def test_sets_repeatable_read_isolation_level(data_access_layer):
    isolation_level = None

    def func(*args, **kwargs):
        nonlocal isolation_level
        isolation_level = kwargs["isolation_level"]
        return data_access_layer.connection

    data_access_layer.connection.execution_options = func

    check_reservation_status_db(data_access_layer)

    assert isolation_level == "SERIALIZABLE"
