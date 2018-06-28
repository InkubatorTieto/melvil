from flask import url_for


def test_edit_pass_get(client, db_user, app_session):
    resp = client.get(url_for('library.edit_password',
                              user_id=db_user.id))
    assert resp.status_code == 200, \
        "Edit password GET view wrong response"


def test_edit_pass_post(client,
                        db_user,
                        password_edition_form,
                        app_session):
    resp = client.post(url_for('library.edit_password',
                            user_id=db_user.id,
                            data=password_edition_form.data))
    assert resp.status_code == 200, \
        "Edit password POST view wrong response"
