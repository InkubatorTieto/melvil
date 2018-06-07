import pytest
from mimesis import Generic
from flask import url_for, request
from app import create_app
from app import db as _db
from app import mail as _mail
from sqlalchemy import event
from models import User, Book, Author

g = Generic('en')


@pytest.fixture(scope='module')
def app():
    """
    Returns flask app with context for testing.
    """
    app = create_app()
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


@pytest.fixture(scope='module')
def user(app):
    data = {
        'email': 'test1@test.com',
        'first_name': 'Testowy',
        'surname': 'test',
        'password': '5354'}
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
def db_author(session, client):
    a = {'first_name': g.person.name(),
         'surname': g.person.surname(),
         'submit': 'Create'
         }
    aa = Author(
        first_name=g.person.name(),
        last_name=g.person.surname()
    )

    client.post(url_for('library_books.add_book'), data=a)
    # client.post(client.post(url_for('library.login'), data=data))
    session.add(aa)
    session.commit()

    yield a

    # if Author.query.filter_by(first_name=a['first_name'], last_name=a['last_name']).first():
    #     session.delete(aa)
    #     session.commit()


@pytest.fixture
def mailbox(app):
    mailbox = _mail.record_messages()
    return mailbox
