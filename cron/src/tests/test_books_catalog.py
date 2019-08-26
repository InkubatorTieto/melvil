from datetime import datetime, timedelta
from notifications.books_catalog import BooksCatalog


class TestBooksCatalog():
    def test_get_overdue_books(self, data_access_layer):
        due_date = datetime(2030, 5, 6) + timedelta(hours=48)

        catalog = BooksCatalog(data_access_layer)
        books = catalog.get_overdue_books(due_date)

        assert len(books) == 3

        assert contains_book(books, 'Very interesing book', '1')
        assert contains_book(books, 'The book part 2', '1')
        assert contains_book(books, 'The book part 2', '2')


def contains_book(books, book_title, borrower_id):
    try:
        next(book for book in books if
             book['book_info']['book_title'] == book_title and
             book['borrower_info']['borrower_id'] == borrower_id)
        return True
    except StopIteration:
        return False
