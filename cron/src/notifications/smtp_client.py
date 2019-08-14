from smtplib import SMTP


class Smtp():
    def __init__(self, host, port, user, password, use_tls=False):
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._use_tls = use_tls

    def send(self, message):
        with _get_smtp_client(
            host=self._host,
            port=self._port
        ) as smtp_client:
            if self._use_tls:
                smtp_client.ehlo()
                smtp_client.starttls()
            else:
                smtp_client.helo()
            smtp_client.send_message(message)


def _get_smtp_client(host, port):
    return SMTP(host=host, port=port)
