from send_email import send_email
from config import DevConfig
from binascii import a2b_uu


def test_send(mailbox):

    with mailbox as outbox:
        send_email('testing',
                   DevConfig.ADMINS[0],
                   ['ktos.ktos@cos.com'],
                   'śśś',
                   None)
        assert len(outbox) == 1
        msg = outbox[0]
        assert msg.subject == "testing"
