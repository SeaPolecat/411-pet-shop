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

    def validate(self) -> None:
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Name must be a non-empty string.")
        
        if not self.age or self.age <= 0 or not isinstance(self.age, int):
            raise ValueError("Age must be a positive integer.")
        
        if not self.breed or not isinstance(self.breed, str):
            raise ValueError("Breed must be a non-empty string.")
        
        if not self.weight or self.weight <= 0 or not isinstance(self.weight, (int, float)):
            raise ValueError("Weight must be a positive number.")
        
        if not self.kid_friendly or not isinstance(self.kid_friendly, (bool)):
            raise ValueError("Kid-friendly must be 1 or 0.")

    def __init__(self, name: str, age: int, breed: str, weight: float, kid_friendly: bool):
        """Initialize a new Boxer instance with basic attributes.

        Args:
            name (str): The boxer's name. Must be unique.
            weight (float): The boxer's weight in pounds. Must be at least 125.
            height (float): The boxer's height in inches. Must be greater than 0.
            reach (float): The boxer's reach in inches. Must be greater than 0.
            age (int): The boxer's age. Must be between 18 and 40, inclusive.

        Notes:
            - The boxer's weight class is automatically assigned based on weight.
            - Fight statistics (`fights` and `wins`) are initialized to 0 by default in the database schema.

        """
        self.name = name
        self.weight = weight
        self.height = height
        self.reach = reach
        self.age = age
        self.fights = 0
        self.wins = 0
        self.weight_class = Boxers.get_weight_class(weight)

    @classmethod
    def get_pet_by_id(cls, pet_id: int) -> "Pet":
        """Retrieve a pet by ID.

        Args:
            pet_id: The ID of the pet.

        Returns:
            Pet: The pet instance.

        Raises:
            ValueError: If the pet with the given ID does not exist.

        """
        logger.info(f"Attempting to retrieve pet with ID {pet_id}")

        try:
            pet = db.session.get(cls, pet_id)

            if not pet:
                logger.info(f"Pet with ID {pet_id} not found")
                raise ValueError(f"Pet with ID {pet_id} not found")

            logger.info(f"Successfully retrieved pet: {pet.name})")
            return pet

        except SQLAlchemyError as e:
            logger.error(f"Database error while retrieving pet by ID {pet_id}: {e}")
            raise