from init_db import db
from models.library import LibraryItem


class Magazine(LibraryItem):
    __tablename__ = 'magazines'
    id = db.Column(db.ForeignKey('library_item.id'), primary_key=True)
    year = db.Column(db.Date)
    issue = db.Column(db.String(32))

    __mapper_args__ = {
        'polymorphic_identity': 'magazine',
    }

    def __str__(self):
        return "'{}' issue: {}/{}".format(
            self.title,
            self.issue,
            self.year
        )

    def __repr__(self):
        return "<Magazine: '{}' tags={} issue={} year={} copies={}>".format(
            self.title,
            self.tags,
            self.issue,
            self.year,
            self.copies
        )
