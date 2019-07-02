from os import getenv
from datetime import datetime
from urllib.parse import quote_plus
from sqlalchemy.sql import select, bindparam
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
        isolation_level="SERIALIZABLE")

    rental_log = dal.rental_log
    copy = dal.copy

    items = None
    with connection.begin():
        items = connection.execute(
            select([
                copy.c.id,
                copy.c.library_item_id,
                rental_log.c.id,
            ])
            .select_from(copy.join(rental_log))
            .where(rental_log.c.book_status == BookStatus.RESERVED)
            .where(rental_log.c._reservation_end <= datetime.utcnow())
        ).fetchall()

        if not items:
            return

        bind_items = [
            {'copy_id': item[0], 'renatl_log_id': item[2]}
            for item in items]

        connection.execute(
            rental_log
            .update()
            .where(rental_log.c.id == bindparam('renatl_log_id'))
            .values(book_status=BookStatus.RETURNED),
            bind_items
        )

        connection.execute(
            copy
            .update()
            .where(copy.c.id == bindparam('copy_id'))
            .values(available_status=BookStatus.RETURNED),
            bind_items
        )

    print("[{}] Cancelled reservation for library item id: {}"
          .format(datetime.now(),
                  ', '.format([item[1] for item in items])))


if __name__ == '__main__':
    load_dotenv()
    data_access_layer = DataAccessLayer(get_url())
    check_reservation_status_db(data_access_layer)
