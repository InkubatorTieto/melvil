from datetime import datetime
from random import randint

import pytz
from mimesis import Generic

from models import (
    RentalLog,
    Copy,
    Book,
    Author,
    Tag,
    User,
    Magazine,
    WishListItem
)


g = Generic('en')


def populate_users(n=20, role=None):
    return [User(
        email=g.person.email(),
        first_name=g.person.name(),
        surname=g.person.surname(),
        password_hash=g.cryptographic.hash(),
        active=g.development.boolean(),
        roles=[role] if role else []
    ) for _ in range(n)]


def populate_books(n=30, authors=None, tags=None):
    return [Book(
        isbn=g.code.isbn(),
        authors=authors if authors else [],
        title=' '.join(g.text.title().split(' ')[:5]),
        original_title=' '.join(g.text.title().split(' ')[:5]),
        publisher=g.business.company(),
        pub_date=g.datetime.datetime().date(),
        language=g.person.language(),
        tags=tags if tags else [],
        description=g.text.sentence()
    ) for _ in range(n)]


def populate_magazines(n=10, tags=None):
    return [Magazine(
        title=' '.join(g.text.title().split(' ')[:5]),
        language=g.person.language(),
        description=g.text.sentence(),
        year=g.datetime.datetime().date(),
        issue=randint(1, 12),
        tags=tags if tags else [],
    ) for _ in range(n)]


def populate_copies(item, n=35):
    return [Copy(
        asset_code='{}{}'.format(
            g.code.locale_code()[:2],
            g.code.pin(mask='######')),
        library_item=item,
        shelf=g.code.pin(),
        has_cd_disk=g.development.boolean()
    ) for _ in range(n)]


def populate_authors(n=40):
    return [Author(
        first_name=g.person.name(),
        last_name=g.person.last_name()
    ) for _ in range(n)]


def populate_tags(n=15):
    return [Tag(
        name=g.text.word()
    ) for _ in range(n)]


def populate_rental_logs(copy_id, user_id, n=30):
    return [RentalLog(
        copy_id=copy_id,
        user_id=user_id,
        borrow_time=datetime.now(tz=pytz.utc),
        return_time=datetime.now(tz=pytz.utc),
    ) for _ in range(n)]


def populate_wish_list_items(n=30, likes=None):
    return [WishListItem(
        authors=g.person.last_name() + g.person.name(),
        title=' '.join(g.text.title().split(' ')[:5]),
        pub_year=datetime.now(tz=pytz.utc),
        likes=likes if likes else [],

    ) for _ in range(n)]
