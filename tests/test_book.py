from flask import session
import datetime
from random import choice, randint
from unittest import mock
import sys

from flask import url_for
from mimesis import Generic
import pytest

from models import Author, Book, Tag, Magazine, LibraryItem
from forms.book import BookForm, MagazineForm


year_now = datetime.datetime.now().year


def test_add_book(view_book, client, login_form_admin_credentials, mock_ldap):
    sys.path.append("..")
    with mock.patch('views.index.ldap_client', mock_ldap):
        view_book.radio.data = 'book'
        client.post(url_for('library.login'),
                    data=login_form_admin_credentials.data)
        client.post(url_for('library_books.add_book'),
                    data=view_book.data,
                    follow_redirects=True)

        author = Author.query.filter_by(
            first_name=view_book.first_name.data,
            last_name=view_book.surname.data
        ).first()

        if not author:
            assert False, "Data validation failed"
        assert view_book.first_name.data == author.first_name \
            and view_book.surname.data == author.last_name, \
            "First and last name of the first author is not" \
            " the same as given at the entrance"

        book = Book.query.filter_by(title=view_book.title.data,
                                    isbn=view_book.isbn.data).first()
        if not book:
            assert False, "Data validation failed"
        assert view_book.title.data == book.title, \
            "The title of the book is not the same as given at the entrance "
        assert view_book.isbn.data == book.isbn, \
            "The ISBN number is not the same as given at the entrance "
        assert view_book.table_of_contents.data == book.table_of_contents, \
            "The table of content is not the same as given at the entrance "
        assert view_book.language.data == book.language, \
            "Language is not the same as given at the entrance "
        assert view_book.category.data == book.category, \
            "Category of book is not the same as given at the entrance "
        assert view_book.description.data == book.description, \
            "The book description is not the same as given at the entrance "
        assert view_book.original_title.data == book.original_title, \
            "The original title of book is not the same as given at the entrance "  # noqa: E501
        assert view_book.publisher.data == book.publisher, \
            "The publisher is not the same as given at the entrance "
        assert datetime.date(
            year=int(view_book.pub_date.data), month=1, day=1
        ) == book.pub_date, \
            "The year of publication is not the same as given at the entrance "

        tag = Tag.query.filter_by(name=view_book.tag.data[0]).first()
        if not tag:
            assert False, "Data validation failed"

        assert tag.name in view_book.tag.data, \
            "Tags ane not the same"
        session.clear()


def test_add_magazine(
    view_magazine, client, login_form_admin_credentials, mock_ldap
):
    with mock.patch('views.index.ldap_client', mock_ldap):
        view_magazine.radio.data = 'magazine'
        client.post(url_for('library.login'),
                    data=login_form_admin_credentials.data)
        client.post(url_for('library_books.add_book'),
                    data=view_magazine.data,
                    follow_redirects=True)

        magazine = Magazine.query\
            .filter_by(
                title=view_magazine.title_of_magazine.data,
                issue=view_magazine.issue.data[0]
            ).first()
        if not magazine:
            assert False, "Data validation failed"
        assert view_magazine.title_of_magazine.data == magazine.title, \
            "The title of the book is not the same as given at the entrance "
        assert view_magazine.table_of_contents.data == \
            magazine.table_of_contents, \
            "The table of content is not the same as given at the entrance "
        assert view_magazine.language.data == magazine.language, \
            "Language is not the same as given at the entrance "
        assert view_magazine.category.data == magazine.category, \
            "Category of book is not the same as given at the entrance "
        assert view_magazine.description.data == magazine.description, \
            "The book description is not the same as given at the entrance "
        assert datetime.date(
            year=int(view_magazine.pub_date.data), month=1, day=1
        ) == magazine.year, \
            "The year of publication is not the same as given at the entrance "
        assert view_magazine.issue.data[0] == magazine.issue, \
            "The book description is not the same as given at the entrance "

        tag = Tag.query.filter_by(name=view_magazine.tag.data[0]).first()
        if not tag:
            assert False, "Data validation failed"
        assert tag.name in view_magazine.tag.data, \
            "Tags ane not the same"
        session.clear()

    def test_add_the_same_book(view_magazine, client):
        client.post(url_for('library_books.add_book'),
                    data=view_magazine.data,
                    follow_redirects=True)

        client.post(url_for('library_books.add_book'),
                    data=view_magazine.data,
                    follow_redirects=True)
        assert not bool(view_magazine.errors), \
            "Two same books have been added."


"""Testing separated validators"""


@pytest.mark.parametrize("values, result", [
    ("", True),
    (".", False),
    ("abc", False),
    ("Fasd.", False),
    ("Pawel", True),
    ("J.J", True),
    ("J.asd", True),
    ("A.Adsa", True),
    ("A.AdsaA", False),
    ("Paweł", True)

])
def test_check_author(view_book, values, result):
    view_book.first_name_1.data = values
    view_book.first_name_1.validate(view_book)
    assert bool(view_book.errors) != result, \
        "The validator 'check_author' returns not" \
        " a valid value\n Errors:{0}".format(view_book.errors)


@pytest.mark.parametrize("values, result", [
    ("polish", True),
    ("english", True),
    ("other", True),
    ("Fasd", False),
    ("aawel", False)

])
def test_check_language(view_book, values, result):
    view_book.language.data = values
    view_book.language.validate(view_book)
    assert bool(view_book.errors) != result, \
        "The validator 'check_language' returns not" \
        " a valid value\n Errors:{0}".format(view_book.errors)


@pytest.mark.parametrize("values, result", [
    ("developers", True),
    ("managers", True),
    ("magazines", True),
    ("other", True),
    ("Other", False)

])
def test_check_category(view_book, values, result):
    view_book.category.data = values
    view_book.category.validate(view_book)
    assert bool(view_book.errors) != result, \
        "The validator 'check_category' returns not" \
        " a valid value\n Errors:{0}".format(view_book.errors)


@pytest.mark.parametrize("values, result", [
    ("978-1-86197-876-9", True),
    ("9781861978769", True),
    ("978-1-86197-87", False),
    ("2-1234-5680-2", True),
    ("2 123 4 5680 2", True),
    ("21234-56802", True),
    ("1-86197 271-7", False),
    ("1 86197 271 7", False),
    ("1 897 271 7", False)

])
def test_check_isbn(view_book, values, result):
    view_book.isbn.data = values
    view_book.isbn.validate(view_book)
    assert bool(view_book.errors) != result, \
        "The validator 'check_isbn' returns not" \
        " a valid value\n Errors:{0}".format(view_book.errors)


@pytest.mark.parametrize("values, result", [
    ("1969", False),
    ("1970", True),
    (str(year_now), True),
    (str(year_now + 1), False),
    (2005, False)

])
def test_check_pub_date(view_book, values, result):
    view_book.pub_date.data = values
    view_book.pub_date.validate(view_book)
    assert bool(view_book.errors) != result, \
        "The validator 'check_pub_date' returns not" \
        " a valid value\n Errors:{0}".format(view_book.errors)


# End of Testing separated validators


def test_update_book(
    view_edit_book, client, login_form_admin_credentials, mock_ldap
):
    with mock.patch('views.index.ldap_client', mock_ldap):
        languages = ['polish', 'english', 'other']
        categories = ['developers', 'managers', 'magazines', 'other']
        g = Generic('en')

        item = LibraryItem.query.filter_by(
            title=view_edit_book.title.data
        ).first()

        form = BookForm(
            radio='book',
            first_name=g.person.name(),
            surname=g.person.surname(),
            title=' '.join(g.text.title().split(' ')[:3]),
            table_of_contents=g.text.sentence(),
            language=choice(languages),
            category=choice(categories),
            tag=g.text.words(1),
            description=g.text.sentence(),
            isbn=str(9789295055025),
            original_title=' '.join(g.text.title().split(' ')[:3]),
            publisher=g.business.company(),
            pub_date=str(randint(1970, 2018))
        )
        client.post(url_for('library.login'),
                    data=login_form_admin_credentials.data)
        client.post(url_for('library_books.edit_book', item_id=item.id),
                    data=form.data,
                    follow_redirects=True)
        tmp_item = LibraryItem.query.filter_by(id=item.id).first()

        assert tmp_item.title == form.title.data, \
            "Book title has not been updated"
        assert tmp_item.authors[0].first_name == form.first_name.data, \
            "Authors first name has not been updated"
        assert tmp_item.authors[0].last_name == form.surname.data, \
            "Authors last name not been updated"
        assert tmp_item.table_of_contents == form.table_of_contents.data, \
            "Book table of contents has not been updated"
        assert tmp_item.language == form.language.data, \
            "Book language has not been updated"
        assert tmp_item.category == form.category.data, \
            "Book category has not been updated"
        assert tmp_item.description == form.description.data, \
            "Book description has not been updated"
        assert tmp_item.isbn == form.isbn.data, \
            "Book isbn has not been updated"
        assert tmp_item.original_title == form.original_title.data, \
            "Book original_title has not been updated"
        assert tmp_item.publisher == form.publisher.data, \
            "Book publisher has not been updated"
        assert tmp_item.pub_date == datetime.date(
            year=int(form.pub_date.data), month=1, day=1
        ), "Book pub_date has not been updated"
        assert tmp_item.tags[0].name == form.tag.data[0], \
            "Book tags has not been updated"
        session.clear()


def test_update_magazine(
    view_edit_magazine, client, login_form_admin_credentials, mock_ldap
):
    with mock.patch('views.index.ldap_client', mock_ldap):
        languages = ['polish', 'english', 'other']
        categories = ['developers', 'managers', 'magazines', 'other']
        g = Generic('en')

        item = LibraryItem.query.filter_by(
            title=view_edit_magazine.title_of_magazine.data).first()

        form = MagazineForm(
            radio='magazine',
            title_of_magazine=' '.join(g.text.title().split(' ')[:3]),
            table_of_contents=g.text.sentence(),
            language=choice(languages),
            category=choice(categories),
            tag=g.text.words(1),
            description=g.text.sentence(),
            pub_date=str(randint(1970, 2018))
        )
        client.post(url_for('library.login'),
                    data=login_form_admin_credentials.data)
        client.post(url_for('library_books.edit_book', item_id=item.id),
                    data=form.data,
                    follow_redirects=True)
        tmp_item = LibraryItem.query.filter_by(id=item.id).first()

        assert tmp_item.title == form.title_of_magazine.data, \
            "Book title has not been updated"
        assert tmp_item.table_of_contents == form.table_of_contents.data, \
            "Book table of contents has not been updated"
        assert tmp_item.language == form.language.data, \
            "Book language has not been updated"
        assert tmp_item.category == form.category.data, \
            "Book category has not been updated"
        assert tmp_item.description == form.description.data, \
            "Book description has not been updated"
        assert tmp_item.year == datetime.date(
            year=int(form.pub_date.data), month=1, day=1
            ), "Book pub_date has not been updated"
        assert tmp_item.tags[0].name == form.tag.data[0], \
            "Book tags has not been updated"
        session.clear()
