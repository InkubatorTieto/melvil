import pytest
from send_email import send_email
from config import DevConfig


@pytest.mark.skip(reason="This needs better test enviroment config.")
def test_send(mailbox):

    with mailbox as outbox:
        send_email('testing',
                   DevConfig.ADMINS[0],
                   ['ktos.ktos@cos.com'],
                   'test',
                   None)
        assert len(outbox) == 1
        msg = outbox[0]
        assert msg.subject == "testing"
