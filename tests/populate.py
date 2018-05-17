from mimesis import Generic, Text
from models.users import User
from models.books import Book, Copy, Author, Tag
import random

t_en = Text('en')

g = Generic('pl')

def populate_db():
    users = populate_users()
    books = populate_books()
    return users, books


def populate_users(n=20):
    users = []
    while len(users) < n:
        email = g.person.email()
        first_name = g.person.name()
        surname = g.person.surname()
        password_hash = g.cryptographic.hash()
        active = g.development.boolean()
        # roles = random.choice(list(RoleEnum.__members__.values()))
        users.append(User(
            email=email,
            first_name=first_name,
            surname=surname,
            password_hash=password_hash,
            active=active))
    return users


def populate_books(n=30):
    books = []
    while len(books) < n:
        isbn = g.code.isbn()
        title = g.development.programming_language()
        original_title = t_en.title()
        publisher = g.business.company()
        pub_date = g.datetime.date()
        language = g.person.language()
        description = g.text.sentence()

        books.append(Book(
            isbn=isbn,
            title=title,
            original_title=original_title,
            publisher=publisher,
            pub_date=pub_date,
            language=language,
            description=description
        ))
    return books


def populate_copy(n=35):
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
