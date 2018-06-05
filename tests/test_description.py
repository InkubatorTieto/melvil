from flask import url_for

from models import LibraryItem


def test_status_code(client, db_book):
    resp = client.get(url_for('item_description.item_description',
                              item_id=db_book.id))
    assert resp.status_code == 200


def test_user_role(db_user, db_roles):
    db_user.roles.append(db_roles[0])
    assert db_user.has_role('ADMIN')


def test_get_item_by_id(db_book):
    item_id = db_book.id
    item = LibraryItem.query.get_or_404(item_id)
    assert item is db_book


def test_book_authors_string(db_book):
    authors_list = []
    if db_book.type == 'book':
        authors_list = db_book.authors_string()
    assert authors_list != []


def test_magazine_authors_string(db_magazine):
    authors_list = []
    if db_magazine.type == 'book':
        authors_list = db_magazine.authors_string()
    assert authors_list == []


def test_types(db_magazine, db_book):
    assert db_magazine.type == 'magazine'
    assert not db_magazine.type == 'book'
    assert db_book.type == 'book'
    assert not db_book.type == 'magazine'
