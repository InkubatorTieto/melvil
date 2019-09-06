from flask import url_for


def test_status_code(client, app_session, db_copies):
    resp = client.get(url_for(
        "library.reserve",
        item_id=0,
        copy_id=db_copies[0].id
    ))
    assert resp.status_code == 302

    for copy in db_copies[4:]:
        resp = client.get(url_for(
            "library.reserve",
            item_id=0,
            copy_id=copy.id
        ))
        assert resp.status_code == 409


def test_reservations_limit(client, app_session, db_copies):
    for i in range(4):
        resp = client.get(url_for(
            "library.reserve",
            item_id=0,
            copy_id=db_copies[i].id
        ))
    print(resp.data)
    assert b'item_description' in resp.data
