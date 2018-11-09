from flask import url_for
from models import Copy
from models.users import Role, RoleEnum
from tests.populate import (
    populate_copies,
    populate_books)


def test_remove_copy(session, db_user, client, app_session):
    user = db_user
    role_admin = Role.query.filter_by(name=RoleEnum.ADMIN).first()
    db_user.roles.append(role_admin)
    books = populate_books(n=5)
    session.add_all(books)
    session.commit()
    copies_before = session.query(Copy).count()
    for book in books:
        copies = populate_copies(book, n=2)
        session.add_all(copies)
        session.commit()
        copies_added = session.query(Copy).count()
        assert copies_before < copies_added, 'copies were not added'
        for copy in copies:
            session.delete(copy)
            session.commit()
            resp = client.post(url_for('library.remove_copy',
                                       item_id=book.id,
                                       copy_id=copy.id,
                                       db_user=user))

            assert resp.status_code == 404, 'copy has not been deleted'
