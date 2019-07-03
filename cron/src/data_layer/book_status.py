from enum import Enum


class BookStatus(Enum):
    RESERVED = 1
    BORROWED = 2
    RETURNED = 3
