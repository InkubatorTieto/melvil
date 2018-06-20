import random
from random import choice, randint
import string

import pytest
from mimesis import Generic
from sqlalchemy import event
from datetime import datetime

from app import create_app
from app import db as _db
from app import mail as _mail
from forms.book import BookForm, MixedForm, MagazineForm
from models import User, Book, Magazine, Copy, WishListItem, Author, Tag
from forms.copy import CopyAddForm, CopyEditForm
from forms.forms import WishlistForm

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
    type_book = ['book', 'magazine']

    form = MixedForm(
        radio=choice(type_book),
        first_name=g.person.name(),
        surname=g.person.surname(),
        title=' '.join(g.text.title().split(' ')[:5]),
        title_of_magazine=' '.join(g.text.title().split(' ')[:5]),
        table_of_contents=g.text.sentence(),
        language=choice(languages),
        category=choice(categories),
        tag=g.text.words(1),
        description=g.text.sentence(),
        isbn=str(1861972717),
        original_title=' '.join(g.text.title().split(' ')[:5]),
        publisher=g.business.company(),
        pub_date=str(randint(1970, 2018)),
        issue=g.text.words(1)
    )

    return form


@pytest.fixture(scope="function")
def view_edit_book(session):
    languages = ['polish', 'english', 'other']
    categories = ['developers', 'managers',
                  'magazines', 'other']

    author = Author(first_name=g.person.name(),
                    last_name=g.person.surname())
    session.add(author)

    tag = Tag(name=g.text.words(1))
    session.add(tag)
    session.commit()
    form = BookForm(
        radio='book',
        first_name=author.first_name,
        surname=author.last_name,
        title=' '.join(g.text.title().split(' ')[:3]),
        table_of_contents=g.text.sentence(),
        language=choice(languages),
        category=choice(categories),
        tag=tag.name,
        description=g.text.sentence(),
        isbn=str(9789295055025),
        original_title=' '.join(g.text.title().split(' ')[:3]),
        publisher=g.business.company(),
        pub_date=str(randint(1970, 2018))
    )

    book = Book(
        title=form.title.data,
        authors=[author],
        table_of_contents=form.table_of_contents.data,
        language=form.language.data,
        category=form.category.data,
        tags=[tag],
        description=form.description.data,
        isbn=form.isbn.data,
        original_title=form.original_title.data,
        publisher=form.publisher.data,
        pub_date=datetime(year=int(form.pub_date.data),
                          month=1,
                          day=1))

    session.add(book)
    session.commit()

    return form


@pytest.fixture(scope="function")
def view_edit_magazine(session):
    languages = ['polish', 'english', 'other']
    categories = ['developers', 'managers',
                  'magazines', 'other']

    tag = Tag(name=g.text.words(1))
    session.add(tag)
    session.commit()
    form = MagazineForm(
        radio='magazine',
        title_of_magazine=' '.join(g.text.title().split(' ')[:3]),
        table_of_contents=g.text.sentence(),
        language=choice(languages),
        category=choice(categories),
        tag=tag.name,
        description=g.text.sentence(),
        pub_date=str(randint(1970, 2018))
    )

    magazine = Magazine(
        title=form.title_of_magazine.data,
        table_of_contents=form.table_of_contents.data,
        language=form.language.data,
        category=form.category.data,
        tags=[tag],
        description=form.description.data,
        year=datetime(year=int(form.pub_date.data),
                      month=1,
                      day=1))

    session.add(magazine)
    session.commit()

    return form


@pytest.fixture(scope="function")
def copy_form(session, client):
    form_add = CopyAddForm(
        asset_code='wr109100',
        has_cd_disk=True,
        shelf='shelf_one'
    )

    form_edit = CopyEditForm(
        asset_code='ab109100',
        has_cd_disk=True,
        available_status=True,
        shelf='shelf_two'
    )

    yield (form_add, form_edit)


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
def view_wish_list(app):
    form = WishlistForm()
    form.authors.data = g.person.surname() + " " + g.person.name()
    form.title.data = ' '.join(g.text.title().split(' ')[:5])
    form.pub_date.data = str(randint(1970, 2018))
    form.type.data = 'book'
    return form


@pytest.fixture(scope="function")
def db_wishlist_item(session):
    """
    Creates and return function-scoped User database entry
    """
    w = WishListItem(authors=g.person.surname() + " " + g.person.name(),
                     title=' '.join(g.text.title().split(' ')[:5]),
                     pub_year=g.datetime.datetime(),
                     item_type='book'
                     )
    session.add(w)
    session.commit()

    yield w

    if WishListItem.query.get(w.id):
        session.delete(w)
        session.commit()
