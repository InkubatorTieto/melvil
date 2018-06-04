# -*- coding: utf-8 -*-
from flask import url_for
from faker import Faker
import random
import string


fake = Faker()


def test_contact(user, client):

    data = {
        'email': user[fake.email()],
        'title': user[text_generator()],
        'message': user[text_generator()]
    }
    resp = client.get(url_for('library.contact'))
    assert resp.status_code == 200

    resp = client.post(url_for('library.contact'), data=data)
    assert resp.status_code == 200

    print(user)
    assert True
