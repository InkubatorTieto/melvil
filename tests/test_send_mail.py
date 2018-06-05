# -*- coding: utf-8 -*-
import pytest
from send_email import send_email
from config import DevConfig
from faker import Faker
import random
import string


fake = Faker()


def text_generator(chars=string.ascii_letters + 'ąćęłóżź \n\t'):
    size = random.randint(25, 40)
    return ''.join(random.choice(chars) for _ in range(size))


#@pytest.mark.skip(reason="This needs better test environment config.")
def test_send(mailbox):

    subject = text_generator()
    with mailbox as outbox:
        send_email(subject,
                   DevConfig.ADMINS[0],
                   [fake.email()],
                   text_generator(),
                   None)
        assert len(outbox) == 1
        msg = outbox[0]
        assert msg.subject == subject
