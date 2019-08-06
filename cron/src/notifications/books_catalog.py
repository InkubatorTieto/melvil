from logging import debug
from sqlalchemy.sql import select
from data_layer.book_status import BookStatus
from .definitions import BookInfo, BorrowerInfo, RecordInfo


class BooksCatalog():
    def __init__(self, data_access_layer):
        self.__data_access_layer = data_access_layer

    def get_overdue_books(self, return_time_delta):
        connection = self.__data_access_layer.connection
        library_item = self.__data_access_layer.library_item
        copy = self.__data_access_layer.copy
        rental_log = self.__data_access_layer.rental_log
        users = self.__data_access_layer.users

        select_stmt = (
            select([
                users.c.employee_id,
                users.c.email,
                users.c.first_name,
                users.c.surname,
                library_item.c.title,
                rental_log.c._borrow_time,
                rental_log.c._return_time
            ])
            .select_from(library_item.join(copy).join(users.join(rental_log)))
            .where(rental_log.c.book_status == BookStatus.BORROWED)
            .where(rental_log.c._return_time <= return_time_delta)
        )

        debug('Executing :\n{}'.format(str(select_stmt)))

        return [
            RecordInfo(
                BorrowerInfo(*item[0:4]),
                BookInfo(*item[4:7])
            ) for item in connection.execute(select_stmt).fetchall()
        ]
