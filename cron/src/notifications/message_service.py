from datetime import datetime
from itertools import groupby
from pystache import render
from email.message import EmailMessage


class MessageService():
    def __init__(self, sender):
        self._sender = sender

    def compose_messages(self, template, books_records):
        now = datetime.utcnow()
        subject = 'Reminder from Melvil Library'

        for key, values in groupby(
                books_records, key=lambda item: item['borrower_info']):
            data = {
                'recipient_name': key['borrower_name'],
                'recipient_surname': key['borrower_surname'],
                'items': [{
                    'borrow_date': item['book_borrow_date'],
                    'title': item['book_title'],
                    'due_date': item['book_due_date'],
                    'days_left': (item['book_due_date'] - now).days}
                    for item in (value['book_info'] for value in values)]
            }

            html_document = render(template, data)

            message = EmailMessage()
            message['From'] = self._sender
            message['To'] = (
                '{} {} <{}>'
                .format(
                    key['borrower_surname'],
                    key['borrower_name'],
                    key['borrower_email'])
            )
            message['Subject'] = subject
            message.set_content(html_document, subtype='html')

            yield message
