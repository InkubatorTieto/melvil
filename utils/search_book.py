from sqlalchemy import or_
from models import Author, LibraryItem


def search_book(query_str):
    query_words = list(map(
        lambda x: '%{}%'.format(x),
        query_str.split()
    ))
    items_id = []
    for word in query_words:
        title_search = LibraryItem.query.filter(
            LibraryItem.title.ilike(word)
        ).all()
        author_search = _search_by_author(word)
        items_id += [item.id for item in title_search + author_search]
    return LibraryItem.id.in_(items_id)


def _search_by_author(query_str):
    author_search = Author.query.filter(
        or_(
            Author.first_name.ilike(query_str),
            Author.last_name.ilike(query_str)
        )).all()
    return sum(
        map(lambda x: x.books, author_search),
        []
    )
