import logging
from typing import List

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from pets.db import db
from pets.utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)

class Pet(db.Model):
    """
    Represents a pet available in the pet shop system.

    This model maps to the 'pets' table in the database and stores attributes
    like name, breed, age, weight, size classification, kid-friendliness, and price.
    Used in a Flask-SQLAlchemy application to manage pet data and perform operations
    like adding, retrieving, updating, and deleting pets.
    """

    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    breed = db.Column(db.String, unique=True, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    kid_friendly = db.Column(db.Bool, nullable=False)
    price = db.Column(db.Float, nullable=False)
    size = db.Column(db.String)

    def validate(self) -> None:
        """Validate the pet's attributes.

        Ensures all fields meet business rules:
        - Name and breed must be non-empty strings.
        - Age, weight, and price must be positive numbers.
        - Kid-friendliness must be a boolean.
        - Size must be a non-empty string.

        Raises:
            ValueError: If any attribute does not meet its validation rule.
        """
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
        
        if not self.price or self.price <= 0 or not isinstance(self.price, (int, float)):
            raise ValueError("Price must be a positive number.")
        
        if not self.size or not isinstance(self.size, str):
            raise ValueError("Size must be a non-empty string.")

    def __init__(self, name: str, age: int, breed: str, weight: float, kid_friendly: bool, price: float, size: str):
        """Initialize a new Pet instance with the given attributes.

        Args:
            name (str): The pet's name. Must be unique.
            age (int): The pet's age in years. Must be positive.
            breed (str): The breed of the pet. Must be unique.
            weight (float): The pet's weight in pounds. Must be positive.
            kid_friendly (bool): Whether the pet is kid-friendly.
            price (float): The price of the pet. Must be positive.
            size (str, optional): The size classification (SMALL, MEDIUM, etc.). 
                If not provided, it is determined automatically based on weight.

        Notes:
            - The pet's size classification is automatically determined if not provided.
        """
        self.name = name
        self.age = age
        self.breed = breed
        self.weight = weight
        self.kid_friendly = kid_friendly
        self.price = price
        self.size = Pet.get_size(weight)

    @classmethod
    def get_size(cls, weight: float) -> str:
        """Determine the size classification based on weight.

        Args:
            weight (float): The pet's weight.

        Returns:
            str: One of 'SMALL', 'MEDIUM', 'LARGE', 'XLARGE'.

        Raises:
            ValueError: If the weight is negative.
        """
        if weight >= 90:
            size = 'XLARGE'
        elif weight >= 55:
            size = 'LARGE'
        elif weight >= 20:
            size = 'MEDIUM'
        elif weight >= 0:
            size = 'SMALL'
        else:
            raise ValueError(f"Invalid weight: {weight}. Weight must be at least 0.")
        return size    

    @classmethod
    def create_pet(cls, name: str, breed: str, age: int, weight: float, kid_friendly: bool) -> None:
        """Create and persist a new Pet instance.

        Args:
            name (str): The pet's name.
            breed (str): The pet's breed.
            age (int): The pet's age.
            weight (float): The pet's weight.
            kid_friendly (bool): Whether the pet is kid-friendly.
            price (float): The price of the pet.

        Raises:
            ValueError: If validation fails or a pet with the same name exists.
            SQLAlchemyError: If there is a database error during creation.

        """
        logger.info(f"Creating pet: {name}, {breed=} {age=} {weight=} {kid_friendly=}")

        try:
            pet = Pet(
                name=name.strip(),
                weight=weight,
                age=age,
                breed=breed.strip(),
                age=age
            )
            pet.validate()
        except ValueError as e:
            logger.warning(f"Validation failed: {e}")
            raise

        try:
            existing = Pet.query.filter_by(name=name.strip()).first()

            if existing:
                logger.error(f"Pet already exists: {name})")
                raise ValueError(f"Pet with name '{name}' already exists.")
            
            db.session.add(pet)
            db.session.commit()
            logger.info(f"Pet successfully added: {name})")

            logger.info(f"Pet created successfully: {name}")

        except IntegrityError:
            logger.error(f"Pet with name '{name}' already exists.")
            db.session.rollback()
            raise ValueError(f"Pet with name '{name}' already exists.")

        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error during creation: {e}")
            raise

    @classmethod
    def get_pet_by_id(cls, pet_id: int) -> "Pet":
        """Retrieve a pet by its ID.

        Args:
            pet_id (int): The pet's ID.

        Returns:
            Pet: The pet instance.

        Raises:
            ValueError: If no pet is found with the given ID.
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

    @classmethod
    def get_pet_by_name(cls, name: str) -> "Pet":
        """Retrieve a pet by its name.

        Args:
            name (str): The pet's name.

        Returns:
            Pet: The pet instance.

        Raises:
            ValueError: If no pet is found with the given name.
        """
        logger.info(f"Attempting to retrieve pet with name '{name}'")

        try:
            pet = cls.query.filter_by(name=name.strip()).first()

            if not pet:
                logger.info(f"Pet with name '{name}'")
                raise ValueError(f"Pet with name '{name}' not found")

            logger.info(f"Successfully retrieved pet: {pet.name})")
            return pet

        except SQLAlchemyError as e:
            logger.error(
                f"Database error while retrieving pet by name "
                f"(name '{name}): {e}"
            )
            raise

    @classmethod
    def delete(cls, pet_id: int) -> None:
        """Delete a pet by its ID.

        Args:
            pet_id (int): The pet's ID.

        Raises:
            ValueError: If no pet is found with the given ID.
            SQLAlchemyError: If any database error occurs during deletion.
        """
        logger.info(f"Received request to delete pet with ID {pet_id}")

        try:
            pet = cls.query.get(pet_id)
            if not pet:
                logger.warning(f"Attempted to delete non-existent pet with ID {pet_id}")
                raise ValueError(f"Pet with ID {pet_id} not found")

            db.session.delete(pet)
            db.session.commit()
            logger.info(f"Successfully deleted pet with ID {pet_id}")

        except SQLAlchemyError as e:
            logger.error(f"Database error while deleting pet with ID {pet_id}: {e}")
            db.session.rollback()
            raise

    
    def update_price(self, new_price: float) -> None:
        """Update the pet's price.

        Args:
            new_price: The pet's new price.

        Raises:
            ValueError: If the new price is invalid.
            SQLAlchemyError: If any database error occurs.
        """
        logger.info(f"Attempting to update price for pet with name {self.name}")

        try:
            if new_price <= 0:
                raise ValueError("Price must be a positive number. Pets can't be free!")

            self.price = new_price

            db.session.commit()
            logger.info(f"Updated price for pet {self.name}: ${self.price}.")

        except SQLAlchemyError as e:
            logger.error(f"Database error while updating price for pet {self.name}: {e}")
            db.session.rollback()
            raise