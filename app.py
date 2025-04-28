from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, Response, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_cors import CORS

from config import ProductionConfig

from pets.db import db
from pets.models.pet_model import Pet
from pets.models.user_model import Users
from pets.utils.logger import configure_logger
from pets.utils.api_utils import get_image

load_dotenv()

def create_app(config_class=ProductionConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)


    db.init_app(app)
    CORS(app)

    @app.route('/api/health', methods=['GET'])
    def healthcheck():
        app.logger.info("Health check endpoint hit")
        return jsonify({'status': 'success', 'message': 'Service is running'})

    #Route to list all the pets
    @app.route('api/pets',methods=['GET'])
    def get_pets():
        try:
            pets = Pet.query.all()
            pets_list = [{
                'id': pet.id,
                'name': pet.name,
                'age': pet.age,
                'breed': pet.breed,
                'weight': pet.weight,
                'kid_friendly': pet.kid_friendly,
                'price': pet.price,
                'size': pet.size,
                'image': pet.image
            } for pet in pets]
            return jsonify(pets_list)
        except Exception as e:
            app.logger.error(f"Error fetching pets: {e}")
            return jsonify({'status': 'error', 'message': 'Error fetching pets'}), 500

    #Route to get Pet IDs to identify the pet
    @app.route('/api/get-pet-by-id/<int:pet_id>', methods=['GET'])
    def get_pet(pet_id):
        try:
            pet = Pet.get_pet_by_id(pet_id)
            pet_data = {
                'id': pet.id,
                'name': pet.name,
                'age': pet.age,
                'breed': pet.breed,
                'weight': pet.weight,
                'kid_friendly': pet.kid_friendly,
                'price': pet.price,
                'size': pet.size,
                'image': pet.image
            }
            return jsonify(pet_data)
        except ValueError as e:
            app.logger.warning(f"Pet with ID {pet_id} not found: {e}")
            return jsonify({'status': 'error', 'message': str(e)}), 404
        except Exception as e:
            app.logger.error(f"Error fetching pet with ID {pet_id}: {e}")
            return jsonify({'status': 'error', 'message': 'Error fetching pet'}), 500

    # Route to add a new pet
    @app.route('/api/add-pet', methods=['POST'])
    def add_pet():
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'Invalid JSON data'}), 400

        try:
            name = data.get('name')
            age = data.get('age')
            breed = data.get('breed')
            weight = data.get('weight')
            kid_friendly = data.get('kid_friendly')
            price = data.get('price')

            # get the image from dog api
            image = get_image(breed)

            if not all([name, age, breed, weight is not None, kid_friendly is not None, price is not None]):
                 return jsonify({'status': 'error', 'message': 'Missing required pet data'}), 400

            Pet.create_pet(name=name, breed=breed, age=age, weight=weight, kid_friendly=kid_friendly, price=price, image=image) 
            return jsonify({'status': 'success', 'message': 'Pet added successfully'}), 201
        except ValueError as e:
            app.logger.warning(f"Error adding pet: {e}")
            return jsonify({'status': 'error', 'message': str(e)}), 400
        except Exception as e:
            app.logger.error(f"Error adding pet: {e}")
            return jsonify({'status': 'error', 'message': 'Error adding pet'}), 500
            
    # Route to delete a new pet
    @app.route('/api/delete-pet/<int:pet_id>', methods=['DELETE'])
    def delete_pet(pet_id):
        try:
            Pet.delete(pet_id) 
            return jsonify({'status': 'success', 'message': f'Pet with ID {pet_id} deleted successfully'})
        except ValueError as e:
            app.logger.warning(f"Pet with ID {pet_id} not found for deletion: {e}")
            return jsonify({'status': 'error', 'message': str(e)}), 404
        except Exception as e:
            app.logger.error(f"Error deleting pet with ID {pet_id}: {e}")
            return jsonify({'status': 'error', 'message': 'Error deleting pet'}), 500

    # Route to update a pet's price by ID
    @app.route('/api/update-price/<int:pet_id>/price', methods=['PUT'])
    def update_pet_price(pet_id):
        data = request.get_json()
        if not data or 'new_price' not in data:
            return jsonify({'status': 'error', 'message': 'Invalid JSON data or missing new_price'}), 400

        new_price = data.get('new_price')

        try:
            pet = Pet.get_pet_by_id(pet_id) 
            pet.update_price(new_price)
            return jsonify({'status': 'success', 'message': f'Price for pet with ID {pet_id} updated successfully'})
        except ValueError as e:
            app.logger.warning(f"Error updating price for pet with ID {pet_id}: {e}")
            return jsonify({'status': 'error', 'message': str(e)}), 400
        except Exception as e:
            app.logger.error(f"Error updating price for pet with ID {pet_id}: {e}")
            return jsonify({'status': 'error', 'message': 'Error updating pet price'}), 500

    #Route to get dog photo depending on the breed
    @app.route('/api/dog_photo', methods=['GET'])
    def get_dog_photo():
        breed = request.args.get('breed')
        if not breed:
            return jsonify({'status': 'error', 'message': 'Breed parameter is required'}), 400
        try:
            photo_url = get_image(breed)
            return jsonify({'status': 'success', 'breed': breed, 'photo_url': photo_url})
        except Exception as e:
            app.logger.error(f"Error fetching dog photo for breed {breed}: {e}")
            return jsonify({'status': 'error', 'message': f'Error fetching dog photo: {e}'}), 500
    return app
    
if __name__ == '__main__':
    app = create_app()
    app.logger.info("Starting Flask app...")
    try:
        app.run(debug=True, host='0.0.0.0', port=5002)
    except Exception as e:
        app.logger.error(f"Flask app encountered an error: {e}")
    finally:
        app.logger.info("Flask app has stopped.")
