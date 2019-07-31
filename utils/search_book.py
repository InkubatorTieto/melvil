from flask import abort
from sqlalchemy import or_, select
from models import Author, LibraryItem, Book


def search_book(query_str):
    query_str = 'jiri'
    query_words = query_str.split()
    items_id = []
    for word in query_words:
        title_search = LibraryItem.query.filter(
            LibraryItem.title.ilike('%{}%'.format(word))
        ).all()
        author_name_search = Author.query.filter(
            Author.first_name.ilike('%{}%'.format(word))
        ).all()
        for search_result in [title_search, author_name_search]:
            items_id += [item.id for item in search_result]

    print('#########')
    print(items_id)
    # title_search = LibraryItem.title.ilike(
    #     '%{}%'.format(query_str)
    # )
    # query = [string.capitalize() for string in query_str.split()]
    # authors = Author.query.filter(
    #     or_(Author.first_name.in_(query), Author.last_name.in_(query))
    # ).all()
    # authors_search = LibraryItem.id.in_(
    #     book.id for book in sum((author.books for author in authors), [])
    # )
    # return or_(title_search, authors_search)
