from flask import abort
from sqlalchemy import or_
from models import Author, LibraryItem


def search_book(search_by, query_str):
    if search_by == 'title':
        return LibraryItem.title.ilike(
            '%{}%'.format(query_str)
        )
    elif search_by == 'author':
        query = [string.capitalize() for string in query_str.split()]
        authors = Author.query.filter(
            or_(Author.first_name.in_(query), Author.last_name.in_(query))
        ).all()
        books = LibraryItem.id.in_(
            book.id for book in sum((author.books for author in authors), [])
        )
        return books
    else:
        abort(404)
