import pytest
from pets.db import db
from app import create_app
from config import TestConfig

@pytest.fixture(scope='session')
def app():
    app = create_app(config_class=TestConfig)
    with app.app_context():
        yield app

@pytest.fixture(scope='session')
def _db(app):
    db.init_app(app)
    db.create_all()
    yield db
    db.drop_all()

@pytest.fixture(scope='function')
def session(_db):
    """Creates a new database session for a test."""
    connection = _db.engine.connect()
    transaction = connection.begin()
    options = dict(bind=connection, binds={})
    session = _db.create_scoped_session(options=options)
    _db.session = session
    yield session
    transaction.rollback()
    connection.close()
    session.remove()
