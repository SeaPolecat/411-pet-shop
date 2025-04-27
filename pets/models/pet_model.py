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
    price = db.Column(db.Float, nullable=False)
    size = db.Column(db.String)

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
        
        if not self.price or self.price <= 0 or not isinstance(self.price, (int, float)):
            raise ValueError("Price must be a positive number.")
        
        if not self.size or not isinstance(self.size, str):
            raise ValueError("Size must be a non-empty string.")

    def __init__(self, name: str, age: int, breed: str, weight: float, kid_friendly: bool, price: float, size: str):
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
        self.age = age
        self.breed = breed
        self.weight = weight
        self.kid_friendly = kid_friendly
        self.price = price
        self.size = Pet.get_size(weight)

    @classmethod
    def get_size(cls, weight: float) -> str:
        """Determine the size based on weight.

        This method is defined as a class method rather than a static method,
        even though it does not currently require access to the class object.
        Both @staticmethod and @classmethod would be valid choices in this context;
        however, using @classmethod makes it easier to support subclass-specific
        behavior or logic overrides in the future.

        Args:
            weight: The weight of the pet.

        Returns:
            str: The weight class of the pet.

        Raises:
            ValueError: If the weight is less than 0.

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
        """Create and persist a new Boxer instance.

        Args:
            name: The name of the boxer.
            weight: The weight of the boxer.
            height: The height of the boxer.
            reach: The reach of the boxer.
            age: The age of the boxer.

        Raises:
            IntegrityError: If a boxer with the same name already exists.
            ValueError: If the weight is less than 125 or if any of the input parameters are invalid.
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

    @classmethod
    def get_pet_by_name(cls, name: str) -> "Pet":
        """Retrieve a pet by name.

        Args:
            name: The name of the pet.

        Returns:
            Pet: The pet instance.

        Raises:
            ValueError: If the pet with the given name does not exist.

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
        """Delete a pet by ID.

        Args:
            pet_id: The ID of the boxer to delete.

        Raises:
            ValueError: If the pet with the given ID does not exist.

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