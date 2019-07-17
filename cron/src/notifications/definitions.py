from collections import namedtuple

BorrowerInfo = namedtuple(
    'BorrowerInfo',
    [
        'borrower_id',
        'borrower_email',
        'borrower_name',
        'borrower_surname',
    ]
)

BookInfo = namedtuple(
    'BookInfo',
    [
        'book_title',
        'book_borrow_date',
        'book_due_date'
    ]
)

RecordInfo = namedtuple(
    'RecordInfo',
    [
        'borrower_info',
        'book_info'
    ]
)
