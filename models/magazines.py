from app import db
from models.library import LibraryItem


class Magazine(LibraryItem):

    __tablename__ = 'magazines'
    id = db.Column(db.ForeignKey('library_item.id'), primary_key=True)
    year = db.Column(db.Integer)
    issue = db.Column(db.String(32))

    __mapper_args__ = {
        'polymorphic_identity': 'magazine',
    }
