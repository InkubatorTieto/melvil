from app import db


class Book(db.Model):

    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(128), unique=True)
    authors = db.relationship('Author', secondary='books_authors',
                              lazy='joined', backref='books')
    title = db.Column(db.String(256))
    original_title = db.Column(db.String(256))
    table_of_contents = db.Column(db.String(256))
    publisher = db.Column(db.String(256))
    pub_date = db.Column(db.String(32))
    language = db.Column(db.String(56))
    tags = db.relationship('Tag', secondary='books_tags',
                           lazy='subquery', backref='books')
    description = db.Column(db.Text)
    copies = db.relationship('Copy', backref='books', lazy='select',
                             cascade='delete')

    def __repr__(self):
        return "Book: {}".format(self.title)


class Copy(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    asset_code = db.Column(db.Integer, unique=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'),
                        nullable=False)
    shelf = db.Column(db.String(56))
    cd_disk = db.Column(db.Boolean)
    rental_logs = db.relationship('RentalLog', backref=db.backref('copy'
                                  , lazy='joined'), lazy='dynamic',
                                  cascade='all, delete-orphan')

    def __repr__(self):
        return "Copy: {}".format(self.asset_code)


class Author(db.Model):

    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Strin(64))
    last_name = db.Column(db.String(64))

    def __repr__(self):
        return "Author: {} {}".format(self.first_name, self.last_name)


class Tag(db.Model):

    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return "Tag: {}".format(self.name)


book_tag = db.Table('books_tags', db.Column('book_id', db.Integer,
                    db.ForeignKey('books.id')), db.Column('tag_id',
                    db.Integer, db.ForeignKey('tags.id')))

book_author = db.Table('books_authors', db.Column('author_id',
                       db.Integer, db.ForeignKey('authors.id')),
                       db.Column('book_id', db.Integer,
                       db.ForeignKey('books.id')))