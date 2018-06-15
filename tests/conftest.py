import random
from random import choice, randint
import string

import pytest
from mimesis import Generic
from sqlalchemy import event

from app import create_app
from app import db as _db
from app import mail as _mail
from forms.book import BookForm
from models import User, Book, Magazine, Copy
from tests.populate import (
    populate_users,
    populate_copies,
    populate_authors,
    populate_books,
    populate_rental_logs,
    populate_magazines
)
from models.library import BookStatus


g = Generic('en')


@pytest.fixture(scope='module')
def app():
    """
    Returns flask app with context for testing.
    """
    app = create_app()
    app.config['WTF_CSRF_ENABLED'] = False
    _mail.init_app(app)
    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture
def client(app):
    with app.test_client() as client:
        return client


@pytest.fixture(scope="module", autouse=True)
def db(app):
    """
    Returns module-wide initialised database.
    """
    _db.create_all()

    yield _db


@pytest.fixture(scope="module")
def session(db):
    """
    Returns module-scoped session.
    """
    conn = db.engine.connect()
    txn = conn.begin()

    options = dict(bind=conn, binds={})
    sess = db.create_scoped_session(options=options)

    sess.begin_nested()

    @event.listens_for(sess(), 'after_transaction_end')
    def restart_savepoint(sess2, trans):
        if trans.nested and not trans._parent.nested:
            sess2.expire_all()
            sess.begin_nested()

    db.session = sess
    yield sess

    sess.remove()
    txn.rollback()
    conn.close()


@pytest.fixture
def mailbox(app):
    return _mail.record_messages()


@pytest.fixture(scope='module')
def email_generator(chars=string.ascii_letters + string.digits + '.' + '-'):
    size = random.randint(10, 25)
    return ''.join(random.choice(chars) for _ in range(size)) + '@tieto.com'


@pytest.fixture(scope='module')
def text_generator(chars=string.ascii_letters + 'ąćęłóżź \n\t'):
    size = random.randint(25, 40)
    return ''.join(random.choice(chars) for _ in range(size))


@pytest.fixture(scope='module')
def text_generator_no_whitespaces(chars=string.ascii_letters + 'ąćęłóżź'):
    size = random.randint(25, 40)
    return ''.join(random.choice(chars) for _ in range(size))


@pytest.fixture(scope='module')
def password_generator(chars=string.ascii_letters):
    size = random.randint(10, 25)
    return ''.join(random.choice(chars) for _ in range(size))


@pytest.fixture(scope='module')
def user(app):

    data = {
        'email': g.person.email(),
        'first_name': g.person.name(),
        'surname': g.person.surname(),
        'password': password_generator(),
        'title': text_generator(),
        'message': text_generator()}
    yield data


@pytest.fixture(scope="function")
def db_user(session):
    """
    Creates and return function-scoped User database entry
    """
    u = User(email=g.person.email(),
             first_name=g.person.name(),
             surname=g.person.surname(),
             password_hash=g.cryptographic.hash(),
             active=g.development.boolean(),
             roles=[])
    session.add(u)
    session.commit()

    yield u

    if User.query.get(u.id):
        session.delete(u)
        session.commit()


@pytest.fixture(scope="function")
def db_book(session):
    """
    Creates and return function-scoped Book database entry
    """
    b = Book(isbn=g.code.isbn(),
             authors=[],
             title=' '.join(g.text.title().split(' ')[:5]),
             original_title=' '.join(g.text.title().split(' ')[:5]),
             publisher=g.business.company(),
             pub_date=g.datetime.datetime().date(),
             language=g.person.language(),
             tags=[],
             description=g.text.sentence())
    session.add(b)
    session.commit()

    yield b

    if Book.query.get(b.id):
        session.delete(b)
        session.commit()


@pytest.fixture(scope="function")
def view_book(session, client):
    languages = ['polish', 'english', 'other']
    categories = ['developers', 'managers',
                  'magazines', 'other']

    form = BookForm(
        first_name=g.person.name(),
        surname=g.person.surname(),
        title=' '.join(g.text.title().split(' ')[:5]),
        table_of_contents=g.text.sentence(),
        language=choice(languages),
        category=choice(categories),
        tag=g.text.words(1),
        description=g.text.sentence(),
        isbn=str(1861972717),
        original_title=' '.join(g.text.title().split(' ')[:5]),
        publisher=g.business.company(),
        pub_date=str(randint(1970, 2018))
    )

    yield form


@pytest.fixture(scope="function")
def db_magazine(session):
    m = Magazine(
        title=' '.join(g.text.title().split(' ')[:5]),
        language=g.person.language(),
        description=g.text.sentence(),
        year=g.datetime.datetime(),
        issue=random.randint(1, 12),
        tags=[],
    )
    session.add(m)
    session.commit()

    yield m

    if Magazine.query.get(m.id):
        session.delete(m)
        session.commit()


@pytest.fixture(scope="function")
def db_copies(session, db_book):
    copy_available = Copy(
        asset_code='{}{}'.format(
            g.code.locale_code()[:2],
            g.code.pin(mask='######')),
        library_item=db_book,
        available_status=True
    )
    copy_not_available = Copy(
        asset_code='{}{}'.format(
            g.code.locale_code()[:2],
            g.code.pin(mask='######')),
        library_item=db_book,
        available_status=False
    )
    session.add_all([copy_available, copy_not_available])
    session.commit()

    yield (copy_available, copy_not_available)


@pytest.fixture
def app_session(client, db_user):
    with client.session_transaction() as app_session:
        app_session['logged_in'] = True
        app_session['id'] = db_user.id
        return app_session


@pytest.fixture
def user_reservations(session):
    """
    Creates reservations for one user
    """
    user = populate_users(n=1)
    session.add_all(user)
    session.commit()
    authors = populate_authors(n=2)
    session.add_all(authors)
    session.commit()
    books = populate_books(n=2, authors=authors)
    session.add_all(books)
    session.commit()
    magazines = populate_magazines(n=2)
    session.add_all(magazines)
    session.commit()
    copies = list()
    copies.append(populate_copies(books[0], n=1)[0])
    copies.append(populate_copies(books[1], n=1)[0])
    copies.append(populate_copies(magazines[0], n=1)[0])
    copies.append(populate_copies(magazines[1], n=1)[0])
    session.add_all(copies)
    session.commit()
    reservations = list()
    reservations.append(populate_rental_logs(copies[0].id, user[0].id, n=1)[0])
    reservations.append(populate_rental_logs(copies[1].id, user[0].id, n=1)[0])
    reservations.append(populate_rental_logs(copies[2].id, user[0].id, n=1)[0])
    reservations.append(populate_rental_logs(copies[3].id, user[0].id, n=1)[0])
    session.add_all(reservations)
    session.commit()
    reservations[0].book_status = BookStatus.RESERVED
    reservations[1].book_status = BookStatus.BORROWED
    reservations[2].book_status = BookStatus.RESERVED
    reservations[3].book_status = BookStatus.BORROWED

    yield user[0], (books[0], reservations[0]), (books[1], reservations[1]), \
        (magazines[0], reservations[2]), (magazines[1], reservations[3])
    for r in reservations:
        session.delete(r)
    for c in copies:
        session.delete(c)
    for b in books:
        session.delete(b)
    for m in magazines:
        session.delete(m)
    session.delete(user[0])
    session.commit()
