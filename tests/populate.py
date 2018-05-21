from random import randint

from mimesis import Generic, Text
from models.users import User
from models.books import Book, Copy, Author, Tag
from models.library import RentalLog

t_en = Text('en')
g = Generic('en')


def populate_db():
    users = populate_users()
    books = populate_books()
    copies = populate_copies()
    author = populate_authors()
    tags = populate_tags()
    return users, books, copies, author, tags


def populate_users(n=20, role=None):
    users = []
    while len(users) < n:
        email = g.person.email()
        first_name = g.person.name()
        surname = g.person.surname()
        password_hash = g.cryptographic.hash()
        active = g.development.boolean()
        users.append(User(
            email=email,
            first_name=first_name,
            surname=surname,
            password_hash=password_hash,
            active=active,
            roles=[role] if role else []
        ))
    return users


def populate_books(n=30, authors=None, tags=None):
    books = []
    while len(books) < n:
        isbn = g.code.isbn()
        title = ' '.join(g.text.title().split(' ')[:5])
        original_title = g.text.title()
        publisher = g.business.company()
        pub_date = g.datetime.date()
        language = g.person.language()
        description = g.text.sentence()

        book = Book(
            isbn=isbn,
            authors=authors if authors else [],
            title=title,
            original_title=original_title,
            publisher=publisher,
            pub_date=pub_date,
            language=language,
            tags=tags if tags else [],
            description=description
        )
        books.append(book)
    return books


def populate_copies(book, n=35):
    copies = []
    while len(copies) < n:
        asset_code = g.code.imei()
        shelf = g.code.pin()
        cd_disk = g.development.boolean()

        copies.append(Copy(
            asset_code=asset_code,
            book=book,
            shelf=shelf,
            cd_disk=cd_disk
        ))
    return copies


def populate_authors(n=40):
    authors = []
    while len(authors) < n:
        first_name = g.person.name()
        last_name = g.person.last_name()

        authors.append(Author(
            first_name=first_name,
            last_name=last_name
        ))
    return authors


def populate_tags(n=15):
    tags = []
    while len(tags) < n:
        name = g.text.word()

        tags.append(Tag(
            name=name
        ))
    return tags


def populate_rental_logs(book, user, n=30):
    logs = []
    while len(logs) < n:
        borrow_time = g.datetime.datetime()
        return_time = g.datetime.datetime()
        returned = g.development.boolean()

        logs.append(RentalLog(
            book_copy_id=book,
            user_id=user,
            borrow_time=borrow_time,
            return_time=return_time,
            returned=returned
        ))
    return logs
