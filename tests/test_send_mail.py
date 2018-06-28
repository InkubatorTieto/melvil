from send_email import send_email
from config import DevConfig


def test_send(mailbox,
              text_generator_no_whitespaces,
              email_generator,
              text_generator):

    with mailbox as outbox:
        send_email(text_generator_no_whitespaces,
                   DevConfig.ADMINS[0],
                   [email_generator],
                   text_generator,
                   None)

        msg = outbox[0]

        if (len(outbox) != 1 or
                msg.subject != text_generator_no_whitespaces or
                msg.body != text_generator or
                msg.send_to != {email_generator} or
                msg.sender != DevConfig.ADMINS[0]):

            assert False
