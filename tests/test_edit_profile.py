import re

import pytest
from flask import url_for


def test_edit_prof_get(client, db_user):
    resp = client.get(url_for('library.edit_profile',
                              user_id=db_user.id))
    assert resp.status_code == 200, \
        "Edit profile GET view wrong response"


def test_edit_prof_post(edit_profile_form, client, db_user):
    resp = client.post(url_for('library.edit_profile',
                               user_id=db_user.id),
                       data=edit_profile_form.data)
    assert resp.status_code == 302, \
        "Edit profile POST crashed redirect"


@pytest.mark.parametrize("values, expected", [
    ("abc@tieto.com", True),
    ("qwerty@tieto.com", True),
    ("m2345@buziaczek.pl", False),
    ("mnbk@wp.pl", False),
    ("whazzuup@tieto.com", True)
])
def test_email_regex(values, expected):
    assert bool(re.compile('[0-9A-Za-z-.]*@tieto.com$',
                           flags=re.IGNORECASE)
                .match(values)) == expected, \
        "Regex for email is incorrect"
