from notifications import smtp_client
from unittest.mock import Mock, patch


class TestSmtp():
    def test_send_without_tls_and_without_auth(self):
        smtp = smtp_client.Smtp(
            host='host',
            port='port',
            user=None,
            password=None)
        smtp_client_mock = Mock()

        def smtp_context(port, host):
            return Mock(
                __enter__=lambda x: smtp_client_mock,
                __exit__=Mock())

        with patch('notifications.smtp_client.SMTP', new=smtp_context):
            smtp.send('message')

        smtp_client_mock.helo.assert_called_once()
        smtp_client_mock.starttls.assert_not_called()
        smtp_client_mock.login.assert_not_called()
        smtp_client_mock.send_message.assert_called_once_with('message')

    def test_send_with_tls_and_with_auth(self):
        smtp = smtp_client.Smtp(
            host='host',
            port='port',
            user='user',
            password='password',
            use_tls=True)
        smtp_client_mock = Mock()

        def smtp_context(port, host):
            return Mock(
                __enter__=lambda x: smtp_client_mock,
                __exit__=Mock())

        with patch('notifications.smtp_client.SMTP', new=smtp_context):
            smtp.send('message')

        smtp_client_mock.ehlo.assert_called_once()
        smtp_client_mock.starttls.assert_called_once()
        smtp_client_mock.login.assert_called_once()
        smtp_client_mock.send_message.assert_called_once_with('message')
