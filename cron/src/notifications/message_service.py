from datetime import datetime
from itertools import groupby
from pystache import render

from email.message import EmailMessage


class MessageService():
    def __init__(self, sender):
        self._sender = sender

    def compose_user_messages(self, template, books_records):
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

    def compose_admin_messages(self, template, books_records, admin_emails):

        data = dict(items=[])
        for record in books_records:
            row = {
                'borrower_name': record.borrower_info.borrower_name,
                'borrower_surname': record.borrower_info.borrower_surname,
                'borrower_email': record.borrower_info.borrower_email,
                'book_title': record.book_info.book_title,
                'book_due_date': record.book_info.book_due_date
            }
            data['items'].append(row)

        html_document = render(template, data)

        message = EmailMessage()
        if books_records:
            message['From'] = self.__sender
            message['To'] = ','.join(admin_emails.split())
            message['Subject'] = 'Overdue books'
            message.set_content(html_document, subtype='html')

        return message
