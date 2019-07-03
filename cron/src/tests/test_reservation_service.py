from datetime import datetime
from freezegun import freeze_time

from sqlalchemy.sql import select

from reservations.reservation_service import ReservationService
from data_layer.book_status import BookStatus


@freeze_time(datetime(2030, 5, 6))
def test_clears_reservations_for_outdated_positions(data_access_layer):
    copy = data_access_layer.copy
    rental_log = data_access_layer.rental_log
    connection = data_access_layer.connection

    reservation_service = ReservationService(data_access_layer)
    reservation_service.invalidate_overdue_reservations()

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

    reservation_service = ReservationService(data_access_layer)
    reservation_service.invalidate_overdue_reservations()

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

    reservation_service = ReservationService(data_access_layer)
    reservation_service.invalidate_overdue_reservations()

    assert isolation_level == "SERIALIZABLE"
