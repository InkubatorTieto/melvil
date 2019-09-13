from subprocess import call
from unittest import mock

from config import Config
from models.users import User


def test_admin_list_empty():
    assert Config.ADMIN_LIST


def test_create_admin(mock_ldap):
    with mock.patch('utils.create_admin_user.ldap_client', mock_ldap):
        call(['flask', 'create_admin'])
        email_list = Config.ADMIN_LIST.split()
        check = []
        for email in email_list:
            user = User.query.filter_by(email=email).first()
            try:
                check.append(user.has_role('ADMIN'))
            except AttributeError:
                assert False, 'Admin accounts not created'
        assert check
