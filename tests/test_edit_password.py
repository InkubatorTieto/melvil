from flask import url_for


def test_edit_pass_get(client, db_user, app_session):
    resp = client.get(url_for('library.edit_password',
                              user_id=db_user.id))
    assert resp.status_code == 200, \
        "Edit password GET view wrong response"
