from flask import abort
from sqlalchemy import or_
from sqlalchemy.sql import select, text
from sqlalchemy.sql.expression import func

from models import Author, Book, LibraryItem, book_author
from app import db


# def search_book(query_str):
#     query_words = list(map(
#         lambda x: '%{}%'.format(x),
#         query_str.split()
#     ))
#     items_id = []
#     for word in query_words:
#         title_search = LibraryItem.query.filter(
#             LibraryItem.title.ilike(word)
#         ).all()
#         author_search = _search_by_author(word)
#         items_id += [item.id for item in title_search + author_search]
#     return LibraryItem.id.in_(items_id)


# def _search_by_author(query_str):
#     author_search = Author.query.filter(
#         or_(
#             Author.first_name.ilike(query_str),
#             Author.last_name.ilike(query_str)
#         )).all()
#     return sum(
#         map(lambda x: x.books, author_search),
#         []
#     )


# LibraryItem.query.filter()


def search_book(query_str):
    query_str = '33'
    query_words = list(map(
        lambda x: x.lower(),
        query_str.split()
    ))
    if len(query_words) > 15:
        abort(413)
    search_title = select([LibraryItem.id]).where(
        LibraryItem.title.in_(["%33%"])
    )
    _authors = select([Author.id]).where(
        or_(
            func.lower(Author.first_name).in_(query_words),
            func.lower(Author.last_name).in_(query_words)
        )
    )
    search_author = select([book_author.c.book_id]).where(
        book_author.c.author_id.in_(_authors)
    )
    conn = db.engine.connect()
    # result = conn.execute(search_title)
    # print(result.fetchone())
    search = LibraryItem.id.in_(search_title)
    result = conn.execute(text(
        "SELECT library_item.id FROM library_item  WHERE library_item.title LIKE ('%fajna%', '%ksiazka%')"
    ))
    print(result.fetchall())
    return search
