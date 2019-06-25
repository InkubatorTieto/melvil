from os import getenv
from datetime import datetime
from urllib.parse import quote_plus
from sqlalchemy.sql import select
from sqlalchemy.engine.url import URL
from dotenv import load_dotenv

from data_access_layer import DataAccessLayer, BookStatus


def get_url():
    return URL(
        drivername=getenv("DB_ENGINE"),
        username=getenv("DB_USER"),
        password=quote_plus(getenv("DB_PASSWORD")),
        host=getenv("DB_HOST"),
        port=getenv("DB_PORT"),
        database=getenv("DB_NAME"))


def check_reservation_status_db(dal):
    connection = dal.connection.execution_options(
        isolation_level="REPEATABLE READ")
    rental_log = dal.rental_log
    copy = dal.copy

    with connection.begin():
        items = connection.execute(
            select([
                copy.c.id,
                copy.c.library_item_id,
                rental_log.c.id,
                rental_log.c._reservation_end
                ])
            .select_from(copy.join(rental_log))
            .where(rental_log.c.book_status == BookStatus.RESERVED)
        ).fetchall()
        for copy_id, library_item_id, renatl_log_id, reservation_end in items:
            if True:  # reservation_end <= datetime.now():
                # pylint: disable=no-value-for-parameter
                connection.execute(
                    rental_log
                    .update()
                    .where(rental_log.c.id == renatl_log_id)
                    .values(book_status=BookStatus.RETURNED)
                )
                connection.execute(
                    copy
                    .update()
                    .where(copy.c.id == copy_id)
                    .values(available_status=BookStatus.RETURNED)
                )
                # pylint: enable=no-value-for-parameter
                print("[{}] Cancelled reservation for library item id: {}"
                      .format(datetime.now(), library_item_id))


if __name__ == '__main__':
    load_dotenv()
    data_access_layer = DataAccessLayer(get_url())
    check_reservation_status_db(data_access_layer)
