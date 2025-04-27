import pytest

from pets.models.pet_model import Pet
from app import create_app
from config import TestConfig
from pets.db import db


@pytest.fixture
def sample_pet(session):
    """Fixture to create a sample pet for testing."""
    pet = Pet(
        name="Fluffy",
        age=2,
        breed="Golden Retriever",
        weight=65.0,
        kid_friendly=True,
        price=500.0,
        size="LARGE"
    )
    session.add(pet)
    session.commit()
    return pet


def test_pet_creation(session):
    """Test creating and persisting a new pet."""
    pet = Pet(
        name="Bella",
        age=3,
        breed="Beagle",
        weight=25.0,
        kid_friendly=True,
        price=300.0,
        size="MEDIUM"
    )
    session.add(pet)
    session.commit()

    # Ensure pet was assigned an ID and attributes are set correctly
    assert pet.id is not None
    assert pet.name == "Bella"
    assert pet.size == "MEDIUM"


def test_get_pet_by_id(sample_pet):
    """Test retrieving a pet by ID."""
    pet = Pet.get_pet_by_id(sample_pet.id)
    assert pet.name == "Fluffy"


def test_get_pet_by_name(sample_pet):
    """Test retrieving a pet by name."""
    pet = Pet.get_pet_by_name("Fluffy")
    assert pet.id == sample_pet.id


def test_delete_pet(session, sample_pet):
    """Test deleting a pet and ensuring it's removed."""
    Pet.delete(sample_pet.id)
    # After deletion, retrieving the pet should raise an error
    with pytest.raises(ValueError):
        Pet.get_pet_by_id(sample_pet.id)


def test_update_price(sample_pet):
    """Test updating the price of a pet."""
    sample_pet.update_price(1000.0)
    assert sample_pet.price == 1000.0


def test_invalid_price_update_raises(sample_pet):
    """Test that updating with an invalid (negative) price raises an error."""
    with pytest.raises(ValueError):
        sample_pet.update_price(-10.0)


def test_validate_invalid_data():
    """Test that creating a pet with invalid data raises validation errors."""
    pet = Pet(
        name="", 
        age=0, 
        breed="", 
        weight=0, 
        kid_friendly="yes", 
        price=0, 
        size=""
    )
    with pytest.raises(ValueError):
        pet.validate()

