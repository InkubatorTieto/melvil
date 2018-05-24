import pytest
from app import create_app
# from config import TestConfig
from init_db import db as _db
from sqlalchemy import event


@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config['SECRET_KEY'] = 24

    ctx = app.test_request_context()
    ctx.push()

    yield app



@pytest.fixture(scope='module', autouse=True)
def db(app):
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


@pytest.fixture(scope='module')
def user(app):
    client = app.test_client()
    data = {
        'email': 'test1@test.com',
        'first_name': 'Testowy',
        'surname': 'test',
        'password': '5354',
        'client': client}
    yield data


# @pytest.fixture()
# def teardown(app):
#     ctx = app.app_context()
#     ctx.pop()
