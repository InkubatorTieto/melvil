from unittest import mock

from models import (
    Author,
    Book,
    Copy,
    Magazine,
    User,
    LibraryItem,
    RentalLog,
    BookStatus
)
from utils.xlsx_reader import get_books, get_magazines


def test_loading_from_xlsx(session, mock_ldap):
    with mock.patch('utils.xlsx_reader.ldap_client', mock_ldap):
        get_books('./library_testfile.xlsx')
        get_magazines('./library_testfile.xlsx')
        assert Author.query.filter(Author.last_name == "Rowling").first(),\
            "db does not contain such author"
        assert Author.query.filter(Author.first_name == "J. K.").first(), \
            "db does not contain such author"
        assert Book.query.filter(
            Book.title == 'Harry Potter and the Chamber of Secrets').first(), \
            "book does not exist"
        assert Copy.query.filter(
            Copy.asset_code == "101").first(), \
            "copy does not exist"
        assert Magazine.query.filter(
            LibraryItem.title == 'Forbes').first(), \
            'db does not contain magazine Forbes'
        assert Magazine.query.filter(
            Magazine.year == '2000-01-01').first(), \
            'db does not contain magazine from 2000'
        assert Magazine.query.filter(
            Magazine.issue == '7.0').first(), 'db does not contain issue 7'
        assert len(User.query.all()) == 4, 'user not added to db'
        assert User.query.filter(
            User.first_name == "Pan").first(), 'user first name is incorrect'
        assert User.query.filter(
            User.surname == "Testtest").first(), 'user surname is incorrect'
        assert Copy.query.filter(
            Copy.asset_code == "100"
        ).first().available_status == BookStatus.BORROWED,\
            'book withn asset 100 is not borrowed'
        assert Copy.query.filter(
            Copy.asset_code == "202"
        ).first().available_status == BookStatus.BORROWED,\
            'book withn asset 202 is not borrowed'
        usr_id = User.query.filter(
            User.surname == "Testtest"
        ).first().id
        copy_id_1 = Copy.query.filter(
            Copy.asset_code == "100"
        ).first().id
        assert RentalLog.query.filter(
            RentalLog.user_id == usr_id and
            RentalLog.copy_id == copy_id_1
        ).first().book_status == BookStatus.BORROWED,\
            'copy with asset 100 is not borrowed properly'
        copy_id_2 = Copy.query.filter(
            Copy.asset_code == "202"
        ).first().id
        assert RentalLog.query.filter(
            RentalLog.user_id == usr_id and
            RentalLog.copy_id == copy_id_2
        ).first().book_status == BookStatus.BORROWED,\
            'copy with asset 202 is not borrowed properly'
