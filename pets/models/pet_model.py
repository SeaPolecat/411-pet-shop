import logging
from typing import List

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from pets.db import db
from pets.utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)

class Pet(db.Model):
    """docstring

    """

    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    breed = db.Column(db.String, unique=True, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    kid_friendly = db.Column(db.Bool, nullable=False)

