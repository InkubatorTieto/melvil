from xlsx_reader import (get_books, get_magazines)
from models import (
    Author,
    Book,
    Magazine,
    Copy)


def test_loading_from_xlsx(session):
    get_books('./library_testfile.xlsx')
    get_magazines('./library_testfile.xlsx')
    assert Author.query.filter(Author.last_name == "Rowling"),\
        "db does not contain such author"
    assert Author.query.filter(Author.first_name == "J. K."), \
        "db does not contain such author"
    assert Book.query.filter(
        Book.title == 'Harry Potter and the Chamber of Secrets'), \
        "book does not exist"
    assert Copy.query.filter(
        Copy.asset_code == "101"), \
        "copy does not exist"
    assert Magazine.query.filter(
        Magazine.year == 'Forbes'), \
        'db does not contain magazine Forbes'
    assert Magazine.query.filter(
        Magazine.year == 'Forbes'), \
        'db does not contain magazine Forbes'
    assert Magazine.query.filter(
        Magazine.year == '2000-01-01'), \
        'db does not contain magazine from 2000'
    assert Magazine.query.filter(
        Magazine.issue == '7'), 'db does not contain issue 7'
