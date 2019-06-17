from subprocess import call


from config import Config
from models.users import User


def test_admin_list_empty():
    assert Config.ADMIN_LIST


def test_create_admin():
    call(['flask', 'create_admin'])
    email_list = Config.ADMIN_LIST.split()
    check = []
    for email in email_list:
        user = User.query.filter_by(email=email).first()
        try:
            check.append(user.has_role('ADMIN'))
        except AttributeError:
            assert False, 'Admin accounts not created'
    assert check, 'Admin accounts not created'
    assert all(check)
