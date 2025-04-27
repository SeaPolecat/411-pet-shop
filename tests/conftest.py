import pytest

from app import create_app
from config import TestConfig

@pytest.fixture(scope='session')
def app():
    app = create_app(config_class=TestConfig)
    with app.app_context():
        yield app

@pytest.fixture(scope='session')
def _db(app):
    from pets.db import db
    db.create_all()
    yield db
    db.drop_all()

@pytest.fixture(scope='function')
def session(_db):
    """Creates a new database session for a test."""
    connection = _db.engine.connect()
    transaction = connection.begin()

    yield _db.session  # <-- Use the default session

    transaction.rollback()
    connection.close()
