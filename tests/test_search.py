from flask import url_for

from models.users import RoleEnum, Role

def test_search(client, app_session):

    resp = client.get(url_for('library.search'))
    assert resp.status_code == 200


def test_has_role(db_user):

    role_admin = Role.query.filter_by(name=RoleEnum.ADMIN).first()
    db_user.roles.append(role_admin)
    assert db_user.has_role('ADMIN'), \
        "has_role() method on User model does not work properly"
