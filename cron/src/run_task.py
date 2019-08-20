from argparse import ArgumentParser
from enum import Enum
from sqlalchemy.engine.url import URL
from dotenv import load_dotenv
from os import environ
import logging
from sys import stdout
from datetime import datetime, timedelta

from data_layer.data_access_layer import DataAccessLayer

from notifications.books_catalog import BooksCatalog
from notifications.message_service import MessageService
from notifications.smtp_client import Smtp

from reservations.reservation_service import ReservationService


def send_notifications():
    load_dotenv()

    due_date_diff = environ["NOTIFICATIONS_DUE_DATE_DIFF_HOURS"]
    smtp_host = environ["NOTIFICATIONS_SMPT_HOST"]
    smtp_port = environ["NOTIFICATIONS_SMPT_PORT"]
    smtp_user = environ.get("NOTIFICATIONS_SMPT_USER")
    smtp_password = environ.get("NOTIFICATIONS_SMPT_PASSWORD")
    smtp_sender = environ["NOTIFICATIONS_SMPT_SENDER"]

    due_date = datetime.utcnow() + timedelta(hours=int(due_date_diff))
    database_connection_url = __get_database_connection_url()
    data_access_layer = DataAccessLayer(database_connection_url)

    books_catalog = BooksCatalog(data_access_layer)
    message_service = MessageService(sender=smtp_sender)
    smtp = Smtp(
        host=smtp_host,
        port=smtp_port,
        user=smtp_user,
        password=smtp_password)

    with open('/app/src/notifications/email_template.html') as file_template:
        template = file_template.read()
        records = books_catalog.get_overdue_books(due_date)
        for message in message_service.compose_messages(template, records):
            smtp.send(message)


def invalidate_overdue_reservations():
    load_dotenv()

    database_connection_url = __get_database_connection_url()
    data_access_layer = DataAccessLayer(database_connection_url)

    reservation_service = ReservationService(data_access_layer)
    reservation_service.invalidate_overdue_reservations()


def __get_database_connection_url():
    return URL(
        drivername=environ["DB_ENGINE"],
        username=environ["DB_USER"],
        password=environ["DB_PASSWORD"],
        host=environ["DB_HOST"],
        port=environ["DB_PORT"],
        database=environ["DB_NAME"])


def __setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)-5.5s] %(message)s",
        handlers=[
            logging.StreamHandler(stream=stdout)
        ])


if __name__ == '__main__':
    class TaskType(Enum):
        send_notifications = 'send_notifications'
        invalidate_overdue_reservations = 'invalidate_overdue_reservations'

        def __str__(self):
            return self.value

    __setup_logging()

    logging.info('foo')
    parser = ArgumentParser()
    parser.add_argument(
        'task',
        type=TaskType,
        choices=list(TaskType))
    args = parser.parse_args()

    if args.task == TaskType.invalidate_overdue_reservations:
        invalidate_overdue_reservations()
    else:
        send_notifications()
