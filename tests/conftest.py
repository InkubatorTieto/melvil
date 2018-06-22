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
from models import User, Book, Magazine, Copy, WishListItem
from forms.copy import CopyAddForm, CopyEditForm
from forms.edit_profile import EditProfileForm
from forms.forms import LoginForm, RegistrationForm, ForgotPass
from models import User, Book, Magazine, Copy
from forms.forms import WishlistForm
from tests.populate import (
    populate_users,
    populate_copies,
    populate_authors,
    populate_books,
    populate_rental_logs,
    populate_magazines
)
from models.library import BookStatus
from werkzeug.security import generate_password_hash

g = Generic('en')


@pytest.fixture(scope="module")
def app():
    """
    Returns flask app with context for testing.
    """
    app = create_app()
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["TESTING"] = True
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

    form = BookForm(
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

    yield form


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


@pytest.fixture(scope="function")
def edit_profile_form(session, client):
    f_name = g.person.name()
    surname = g.person.surname()
    mail = f_name + surname + "@tieto.com"
    form_edit = EditProfileForm(
        first_name=f_name,
        surname=surname,
        email=mail
    )

    yield (form_edit)


@pytest.fixture(scope="function")
def db_tieto_user(session):
    """
    Creates and return function-scoped Tieto user database entry
    """
    password = g.person.password(length=8)
    u = User(email=g.person.name() + g.person.surname() + '.' + '@tieto.com',
             first_name=g.person.name(),
             surname=g.person.surname(),
             password_hash=generate_password_hash(password),
             active=True,
             roles=[])
    session.add(u)
    session.commit()

    yield u, password

    if User.query.get(u.id):
        session.delete(u)
        session.commit()


@pytest.fixture(scope="function")
def login_form(db_tieto_user):
    """
    Returns login form containing valid data of registered user.
    """
    form = LoginForm(
        email=User.query.filter_by(id=db_tieto_user[0].id).first().email,
        password=db_tieto_user[1],
    )
    yield form


@pytest.fixture(scope="function")
def login_form_invalid(db_tieto_user):
    """
    Returns login form containing invalid data.
    """
    invalid_password = g.person.password(length=8)
    while(invalid_password == db_tieto_user[1]):
        invalid_password = g.person.password(length=8)

    form = LoginForm(
        email=User.query.filter_by(id=db_tieto_user[0].id).first().email,
        password=invalid_password,
    )
    yield form


@pytest.fixture(scope="function")
def registration_form():
    """
    Returns registration form containing valid data.
    """
    new_password = g.person.password(length=8)
    form = RegistrationForm(
        email=g.person.name() + '.' + g.person.surname() + '@tieto.com',
        first_name=g.person.name(),
        surname=g.person.surname(),
        password=new_password,
        confirm_pass=new_password,
    )
    yield form


@pytest.fixture(scope="function")
def registration_form_registered_user(db_tieto_user):
    """
    Returns registration form containing data of already registered user.
    """
    form = RegistrationForm(
        email=User.query.filter_by(id=db_tieto_user[0].id).first().email,
        first_name=User.query.filter_by
        (id=db_tieto_user[0].id).first().first_name,
        surname=User.query.filter_by(id=db_tieto_user[0].id).first().surname,
        password=db_tieto_user[1],
        confirm_pass=db_tieto_user[1],
    )
    yield form


@pytest.fixture(scope="function")
def registration_form_invalid():
    """
    Returns registration form containing invalid data
    """
    form = RegistrationForm(
        email=g.person.name() + '.' + g.person.surname() + '@gmail.com',
        first_name=g.person.name(),
        surname=g.person.surname(),
        password=g.cryptographic.hash(),
        confirm_pass=g.cryptographic.hash(),
    )
    yield form


@pytest.fixture(scope="function")
def forgot_pass(db_tieto_user):
    """
    Returns password reset form
    """
    form = ForgotPass(
        email=User.query.filter_by(id=db_tieto_user[0].id).first().email,
        submit=True
    )
    yield form


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
    copies = []
    copies.append(populate_copies(books[0], n=1)[0])
    copies.append(populate_copies(books[1], n=1)[0])
    copies.append(populate_copies(magazines[0], n=1)[0])
    copies.append(populate_copies(magazines[1], n=1)[0])
    session.add_all(copies)
    session.commit()
    reservations = []
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
