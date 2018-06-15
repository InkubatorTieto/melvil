from xlsx_reader import (get_books, get_magazines)
from models import (
    Author,
    Book,
    Magazine,
    Copy)


def test_author_name(session):
    get_books('./testfile.xlsx')
    assert Author.query.filter(Author.last_name == "Rowling"),\
        "db does not contain such author"
    assert Author.query.filter(Author.first_name == "J. K."), \
        "db does not contain such author"


def test_book_title(session):
    get_books('./testfile.xlsx')
    assert Book.query.filter(
        Book.title == 'Harry Potter and the Chamber of Secrets'), \
        "book does not exist"


def test_book_copy(session):
    get_books('./testfile.xlsx')
    assert Copy.query.filter(
        Copy.asset_code == "101"), \
        "copy does not exist"


def test_magazine_title(session):
    get_magazines('./testfile.xlsx')
    assert Magazine.query.filter(
        Magazine.year == 'Forbes'), \
        'db does not contain magazine Forbes'


def test_magazine_year(session):
    get_magazines('./testfile.xlsx')
    assert Magazine.query.filter(
        Magazine.year == '2000-01-01'), \
        'db does not contain magazine from 2000'


def test_magazine_issue(session):
    get_magazines('./testfile.xlsx')
    assert Magazine.query.filter(
        Magazine.issue == '7'), 'db does not contain issue 7'
