from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, Response, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
# from flask_cors import CORS

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

    # Initialize SQLAlchemy here
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
                'size': pet.size
            } for pet in pets]
            return jsonify(pets_list)
         except Exception as e:
            app.logger.error(f"Error fetching pets: {e}")
            return jsonify({'status': 'error', 'message': 'Error fetching pets'}), 500
#Route to get Pet IDs to identify the pet
      @app.route('/api/pets/<int:pet_id>', methods=['GET'])
    def get_pet(pet_id):
        try:
            pet = Pet.get_pet_by_id(pet_id) # Fetch a specific pet by ID
            pet_data = {
                'id': pet.id,
                'name': pet.name,
                'age': pet.age,
                'breed': pet.breed,
                'weight': pet.weight,
                'kid_friendly': pet.kid_friendly,
                'price': pet.price,
                'size': pet.size
            }
            return jsonify(pet_data)
        except ValueError as e:
            app.logger.warning(f"Pet with ID {pet_id} not found: {e}")
            return jsonify({'status': 'error', 'message': str(e)}), 404
        except Exception as e:
            app.logger.error(f"Error fetching pet with ID {pet_id}: {e}")
            return jsonify({'status': 'error', 'message': 'Error fetching pet'}), 500
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
