from notifications import smtp_client
from unittest.mock import Mock


class TestSmtp():
    def test_send_without_tls(self):
        smtp = smtp_client.Smtp(
            host='host',
            port='port',
            user='user',
            password='password')
        smtp_client_mock = Mock()

        def context_manager_getter(port, host):
            return Mock(
                __enter__=lambda x: smtp_client_mock,
                __exit__=Mock())

        smtp_client._get_smtp_client = context_manager_getter

        smtp.send('message')

        smtp_client_mock.helo.assert_called_once()
        smtp_client_mock.starttls.assert_not_called()
        smtp_client_mock.send_message.assert_called_once_with('message')

    def test_send_with_tls(self):
        smtp = smtp_client.Smtp(
            host='host',
            port='port',
            user='user',
            password='password',
            use_tls=True)
        smtp_client_mock = Mock()

        def context_manager_getter(port, host):
            return Mock(
                __enter__=lambda x: smtp_client_mock,
                __exit__=Mock())

        smtp_client._get_smtp_client = context_manager_getter

        smtp.send('message')

        smtp_client_mock.ehlo.assert_called_once()
        smtp_client_mock.starttls.assert_called_once()
