from os import getenv
from datetime import datetime
from sqlalchemy.sql import select, update
from dotenv import load_dotenv

from data_access_layer import data_access_layer, BookStatus

def get_connection_string():
    load_dotenv()
    DB_ENGINE = getenv("DB_ENGINE")
    DB_USER = getenv("DB_USER")
    DB_PASSWORD = getenv("DB_PASSWORD")
    DB_HOST = getenv("DB_HOST")
    DB_PORT = getenv("DB_PORT")
    DB_NAME = getenv("DB_NAME")

    return "{0}://{1}:{2}@{3}:{4}/{5}".format(
        DB_ENGINE, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
    )

def check_reservation_status_db(dal):
    connection = dal.connection.execution_options(isolation_level="REPEATABLE READ")
    rental_log = dal.rental_log
    copy = dal.copy

    with connection.begin():
        items = connection.execute(
            select([copy.c.id, rental_log.c.id, rental_log.c._reservation_end]).select_from(
                copy.join(rental_log)).where(rental_log.c.book_status == BookStatus.RESERVED
            )
        ).fetchall()
        for copy_id, renatl_log_id, reservation_end in items:
            if reservation_end <= datetime.now():
                # pylint: disable=no-value-for-parameter
                connection.execute(rental_log.update().where(rental_log.c.id == renatl_log_id).values(book_status=BookStatus.RETURNED))
                connection.execute(copy.update().where(copy.c.id == copy_id).values(available_status=BookStatus.RETURNED))
                # pylint: enable=no-value-for-parameter

if __name__ == '__main__':
    print("---")
    connection_string = get_connection_string()
    data_access_layer.init(connection_string)
    check_reservation_status_db(data_access_layer)
