from datetime import datetime
from logging import debug, info

from sqlalchemy.sql import bindparam, select

from data_layer.book_status import BookStatus


class ReservationService():
    def __init__(self, data_access_layer):
        self._data_access_layer = data_access_layer

    def invalidate_overdue_reservations(self):
        connection = self._data_access_layer.connection
        rental_log = self._data_access_layer.rental_log
        copy = self._data_access_layer.copy

        connection = connection.execution_options(
            isolation_level="SERIALIZABLE")

        items = None
        with connection.begin():
            select_stmt = (
                select([
                    copy.c.id,
                    copy.c.library_item_id,
                    rental_log.c.id,
                ])
                .select_from(copy.join(rental_log))
                .where(rental_log.c.book_status == BookStatus.RESERVED)
                .where(rental_log.c._reservation_end <= datetime.utcnow())
            )

            debug('Executing: \n{}'.format(str(select_stmt)))

            items = connection.execute(select_stmt).fetchall()

            if not items:
                debug('No reservations to cancel.')
                return

            bind_items = [
                {'copy_id': item[0], 'renatl_log_id': item[2]}
                for item in items]

            update_rental_log_stmt = (
                rental_log
                .update()
                .where(rental_log.c.id == bindparam('renatl_log_id'))
                .values(book_status=BookStatus.RETURNED)
            )

            debug('Executing: \n{}'.format(str(update_rental_log_stmt)))
            connection.execute(update_rental_log_stmt, bind_items)

            update_copy_stmt = (
                copy
                .update()
                .where(copy.c.id == bindparam('copy_id'))
                .values(available_status=BookStatus.RETURNED)
            )

            debug('Executing: \n{}'.format(str(update_copy_stmt)))
            connection.execute(update_copy_stmt, bind_items)

        info("[{}] Cancelled reservation for library item id: {}"
             .format(datetime.now(),
                     ', '.join([str(item[1]) for item in items])))
