from models import LibraryItem
from models.users import RoleEnum, Role


def test_user_role(db_user):
    role_admin = Role.query.filter_by(name=RoleEnum.ADMIN).first()
    db_user.roles.append(role_admin)
    assert db_user.has_role('ADMIN'),\
        "has_role() method on User model does not work properly"


def test_get_item_by_id(db_book):
    item_id = db_book.id
    item = LibraryItem.query.get_or_404(item_id)
    assert item is db_book,\
        "Library Item is not returned correctly by id from db"


def test_book_authors_string(db_book):
    authors_list = []
    if db_book.type == 'book':
        authors_list = db_book.authors_string
    assert authors_list != [],\
        "authors_string() method does not work properly with book type"


def test_magazine_authors_string(db_magazine):
    authors_list = []
    if db_magazine.type == 'book':
        authors_list = db_magazine.authors_string
    assert authors_list == [],\
        "authors_string() method does not work properly with magazine type"


def test_types(db_magazine, db_book):
    assert db_magazine.type == 'magazine',\
        "getting type does not work properly with magazines"
    assert not db_magazine.type == 'book',\
        "getting type does not work properly with magazines"
    assert db_book.type == 'book', \
        "getting type does not work properly with books"
    assert not db_book.type == 'magazine', \
        "getting type does not work properly with books"


def test_copy_available(db_book, db_copies):
    assert db_book.copies[0].available_status,\
        "available_status=True on copy does not work properly with books"
    assert not db_book.copies[1].available_status, \
        "available_status=False on copy does not work properly with books"
