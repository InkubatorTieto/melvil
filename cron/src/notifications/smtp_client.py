from smtplib import SMTP_SSL


class Smtp():
    def __init__(self, host, port, user, password, use_tls=False):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.use_tls = use_tls

    def send(self, message):
        with _get_smtp_client(host=self.host, port=self.port) as smtp_client:
            smtp_client.ehlo()
            if self.use_tls:
                smtp_client.starttls()
            smtp_client.login(user=self.user, password=self.password)
            smtp_client.send_message(message)


def _get_smtp_client(host, port):
    return SMTP_SSL(host=host, port=port)
