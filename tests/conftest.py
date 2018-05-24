import pytest
from app import create_app
from app import db as _db
from sqlalchemy import event
from config import TestConfig


@pytest.fixture(scope='session')
def app():
    """
    Returns flask app with context for testing.
    """
    app = create_app(config=TestConfig)
    ctx = app.app_context()
    ctx.push()
    app.config['SECRET_KEY'] = 24


@pytest.fixture
def user(app):
    app = create_app()
    client = app.test_client()
    data = {
        'email': 'test1@test.com',
        'first_name': 'Testowy',
        'surname': 'test',
        'password': '5354',
        'client': client}
    return data


    yield app

    ctx.pop()


@pytest.fixture(scope="module", autouse=True)
def db(app):
    """
    Returns session-wide initialised database.
    """
    _db.create_all()

    yield _db

    _db.drop_all()


@pytest.fixture(scope="module")
def session(db):
    """
    Returns function-scoped session.
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
