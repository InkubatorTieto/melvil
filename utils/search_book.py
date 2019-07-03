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
        # print(Author.query.filter(Author.first_name.ilike('rex')).first().books)
        authors = Author.query.filter(
            or_(Author.first_name.in_(query), Author.last_name.in_(query))
        ).all()
        books = list()
        for author in authors:
            for book in author.books:
                books.append(book.title)
        return LibraryItem.title.in_(books)

    else:
        abort(404)
