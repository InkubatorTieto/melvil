
import re
from wtforms.validators import ValidationError
from datetime import datetime
from isbnlib import is_isbn10, is_isbn13
from models.books import Book


def email_regex():
    e_mail_regex = '[0-9A-Za-z-.]*@tieto.com$'
    return e_mail_regex


def tieto_email(form, field):
    if not re.compile(email_regex()).match(field.data):
        raise ValidationError('Only Tieto emails are accepted.')


def name(form, field):
    if not re.compile("^[A-ZĄĆĘŁÓŻŹ]?[a-ząćęłóżź]*$").match(field.data):
        raise ValidationError("Insert valid name.")


def surname(form, field):
    if not re.compile(
        "^[A-ZĄĆĘŁÓŻŹ]?[a-ząćęłóżź]*-?[A-ZĄĆĘŁÓŻŹ]?[a-ząćęłóżź]*$"
    ).match(field.data):
        raise ValidationError("Insert valid surname.")


def check_author(form, field):
    if field.data != "":
        if (
            not re.compile(
                "^([A-ZĄĆĘŁÓŻŹ]?.*[A-ZĄĆĘŁÓŻŹa-ząćęłóżź]*" "[a-ząćęłóżź])$"
            ).match(field.data) and
            not re.compile("^[A-ZĄĆĘŁÓŻŹ]?." "[A-ZĄĆĘŁÓŻŹ]$").match(
                field.data
            ) or
            re.compile("^[a-ząćęłóżź]*$").match(field.data)
        ):
            raise ValidationError("Insert valid author name or surname.")


def check_language(form, field):
    languages = ["polish", "english", "other"]
    if field.data not in languages:
        raise ValidationError("Language is unavailable. Select correct!")


def check_category(form, field):
    categories = ["developers", "managers", "magazines", "other"]
    if field.data not in categories:
        raise ValidationError("This category is unavailable. Select correct!")


def check_isbn(form, field):
    field.data = field.data.replace("-", "").replace(" ", "")
    if not is_isbn10(field.data) and not is_isbn13(field.data):
        raise ValidationError("ISBN number is incorrect!")

    if Book.query.filter_by(isbn=field.data).first():
        raise ValidationError("This book is already in the database.")


def check_pub_date(form, field):
    if int(field.data) > datetime.now().year:
        raise ValidationError("Date is incorrect.")

    if int(field.data) < 1970:
        raise ValidationError("Date is incorrect.")

    if type(field.data) != str:
        raise ValidationError("Type of data is incorrect")


def title_book_exists(form, field):
    results = Book.query.filter(Book.title.startswith(field.data[:2])).all()
    for i in results:
        i = str(i.title)
        i = (
            i.replace(" ", "")
            .replace("_", "")
            .replace("-", "")
            .replace(",", "")
            .replace(".", "")
            .lower()
        )
        tmp = str(field.data)
        tmp = (
            tmp.replace(" ", "")
            .replace("_", "")
            .replace("-", "")
            .replace(",", "")
            .replace(".", "")
            .lower()
        )
        if i == tmp:
            raise ValidationError(
                "This book already exists." " This title is in database!"
            )
