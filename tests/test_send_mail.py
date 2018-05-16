from __future__ import with_statement
from app import mail
from emails import *


def test_send(app):

    with mail.record_messages() as outbox:
        send_email('testing', 'tieto.library@gmail.com', ['tieto.library@gmail.com'], 'test', 'test')
        assert len(outbox) == 1
        msg = outbox[0]

        assert msg.subject == "testing"
