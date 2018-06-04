from init_db import db
from models.library import LibraryItem


class Book(LibraryItem):

    __tablename__ = 'books'
    id = db.Column(db.ForeignKey('library_item.id'), primary_key=True)
    isbn = db.Column(db.String(128), unique=True)
    authors = db.relationship('Author',
                              secondary='books_authors',
                              lazy='joined',
                              backref=db.backref('books'))
    original_title = db.Column(db.String(256))
    publisher = db.Column(db.String(256))
    pub_date = db.Column(db.Date)

    __mapper_args__ = {
        'polymorphic_identity': 'book',
    }

    def __init__(self, **kwargs):
        super(Book, self).__init__(**kwargs)

    # def __str__(self):
    #     return "'{}' by {}".format(
    #         self.title,
    #         ', '.join([str(a) for a in self.authors])
    #     )

    # def __repr__(self):
    #     return "<Book: '{}' tags={} authors={} copies={}>".format(
    #         self.title,
    #         self.tags,
    #         self.authors,
    #         self.copies
    #     )

    def __repr__(self):
        return "<Book: '{}' authors={} copies={}>".format(
            self.title,
            self.authors,
            self.copies
        )


class Author(db.Model):

    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return "{}".format(self.full_name)

    def __repr__(self):
        return "<Author: {} {}>".format(self.first_name, self.last_name)


book_author = db.Table('books_authors',
                       db.Column('author_id',
                                 db.Integer,
                                 db.ForeignKey('authors.id')),
                       db.Column('book_id',
                                 db.Integer,
                                 db.ForeignKey('books.id')))
