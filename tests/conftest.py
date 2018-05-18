import pytest
from app import create_app
from app import db as _db
from sqlalchemy import event
from config import TestConfig


@pytest.fixture(scope='module')
def app():
    app = create_app(config=TestConfig)
    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture(scope="module")
def db():
    """
    Returns session-wide initialised database.
    """
    _db.drop_all()
    _db.create_all()

    yield _db


@pytest.fixture(scope="function", autouse=True)
def session(app, db):
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
