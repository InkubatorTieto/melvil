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
        title = g.text.title()
        original_title = g.text.title()
        publisher = g.business.company()
        pub_date = g.datetime.date()
        language = g.person.language()
        description = g.text.sentence()

        books.append(Book(
            isbn=isbn,
            authors=authors if authors else [],
            title=title,
            original_title=original_title,
            publisher=publisher,
            pub_date=pub_date,
            language=language,
            tags=tags if tags else [],
            description=description
        ))
    return books


def populate_copies(n=35):
    copies = []
    while len(copies) < n:
        asset_code = g.code.imei()
        shelf = g.code.pin()
        cd_disk = g.development.boolean()

        copies.append(Copy(
            asset_code=asset_code,
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


def populate_rental_logs(n=30):
    logs = []
    while len(logs) < n:
        borrow_time = g.datetime.datetime()
        return_time = g.datetime.datetime()
        returned = g.development.boolean()

        logs.append(RentalLog(
            borrow_time=borrow_time,
            return_time=return_time,
            returned=returned
        ))
    return logs
