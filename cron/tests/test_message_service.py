import logging
from datetime import datetime
from pytest import fixture
from freezegun import freeze_time
from notifications.message_service import MessageService
from notifications.definitions import RecordInfo, BookInfo, BorrowerInfo


class TestMessageService():
    def test_compose_messages_senders(self, test_data):
        sender = 'foo <foo@example.com>'
        template = '{{recipient_surname}}, {{recipient_name}}'
        service = MessageService(sender)
        messages = list(service.compose_messages(template, test_data))

        def recipient_match(message, recipient_name, recipient_surname):
            return str(message.get_content()) == '{}, {}\n'.format(
                recipient_surname,
                recipient_name)

        for m in messages:
            logging.info(m)

        assert len(messages) == 2
        assert len([
            m for m in messages
            if recipient_match(
                m, 'borrower_name_1', 'borrower_surname_1')]) == 1

        assert len([
            m for m in messages
            if recipient_match(
                m, 'borrower_name_2', 'borrower_surname_2')]) == 1

    def test_compose_messages_from(self, test_data):
        sender = 'foo <foo@example.com>'
        service = MessageService(sender)
        messages = list(service.compose_messages('', test_data))

        assert messages[0]['From'] == 'foo <foo@example.com>'
        assert messages[1]['From'] == 'foo <foo@example.com>'

    def test_compose_messages_to(self, test_data):
        sender = 'foo <foo@example.com>'
        service = MessageService(sender)
        messages = list(service.compose_messages('', test_data))

        assert len([
            m for m in messages if
            m['To'] == 'borrower_surname_1 ' +
                       'borrower_name_1 <borrower_email_1@example.com>']) == 1

        assert len([
            m for m in messages if
            m['To'] == 'borrower_surname_2 ' +
                       'borrower_name_2 <borrower_email_2@example.com>']) == 1

    @freeze_time(datetime(2012, 5, 20))
    def test_compose_messages_items(self, test_data):
        sender = 'foo <foo@example.com>'
        service = MessageService(sender)
        template = '{{#items}}{{title}} {{days_left}} |{{/items}}'
        messages = list(service.compose_messages(template, test_data))

        for m in messages:
            logging.info(m)

        assert len([
            m for m in messages if
            str(m.get_content()) == 'book1 1 |book2 2 |\n']) == 1

        assert len([
            m for m in messages if
            str(m.get_content()) == 'book3 3 |\n']) == 1


@fixture()
def test_data():
    return [
        RecordInfo(
            borrower_info=BorrowerInfo(
                borrower_id='borrower_id_1',
                borrower_email='borrower_email_1@example.com',
                borrower_name='borrower_name_1',
                borrower_surname='borrower_surname_1'),
            book_info=BookInfo(
                book_title='book1',
                book_borrow_date=datetime(2012, 5, 20),
                book_due_date=datetime(2012, 5, 21))
        ),
        RecordInfo(
            borrower_info=BorrowerInfo(
                borrower_id='borrower_id_1',
                borrower_email='borrower_email_1@example.com',
                borrower_name='borrower_name_1',
                borrower_surname='borrower_surname_1'),
            book_info=BookInfo(
                book_title='book2',
                book_borrow_date=datetime(2012, 5, 20),
                book_due_date=datetime(2012, 5, 22))
        ),
        RecordInfo(
            borrower_info=BorrowerInfo(
                borrower_id='borrower_id_2',
                borrower_email='borrower_email_2@example.com',
                borrower_name='borrower_name_2',
                borrower_surname='borrower_surname_2'),
            book_info=BookInfo(
                book_title='book3',
                book_borrow_date=datetime(2012, 5, 20),
                book_due_date=datetime(2012, 5, 23))
        ),
    ]
