from xlsx_reader import (get_books, get_magazines)
from models import (
    Author,
    Book,
    Magazine)


def test_authors(session):
    get_books('./testfile.xlsx')
    assert Author.query.count() == 11, "db does not contain 11 authors"


def test_books(session):
    get_books('./testfile.xlsx')
    assert Book.query.count() == 11, "db does not contain 11 books"


def test_particular_author(session):
    get_books('./testfile.xlsx')
    assert Author.query.filter(
        Author.last_name == 'J.K. Rowling'), "author does not exist"


def test_particular_book(session):
    get_books('./testfile.xlsx')
    assert Book.query.filter(
        Book.title == 'Harry Potter and the Chamber of Secrets'), \
        "book does not exist"


def test_magazines(session):
    get_magazines('./testfile.xlsx')
    assert Magazine.query.count() == 5, "db does not contain 5 magazines"


def test_magazine_year(session):
    get_magazines('./testfile.xlsx')
    assert Magazine.query.filter(
        Magazine.year == '2000-01-01'), \
        'db does not contain magazine from 2017'


def test_magazine_issue(session):
    get_magazines('./testfile.xlsx')
    assert Magazine.query.filter(
        Magazine.issue == '7'), 'db does not contain issue 7'
