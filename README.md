
# 🐾 Pet Shop API

A Flask-based RESTful API for managing a pet shop's inventory of adoptable dogs. The app supports user account creation, login/logout, password management, viewing available pets, adding or removing pets, and fetching dog images by breed from an external API.

---

## 🔧 Setup & Run Instructions

To run the app via Docker:

```bash
bash run_docker.sh
```

Or to run manually:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

---

## 🛣️ API Routes

### 1. `/api/health`

- **Method**: `GET`
- **Purpose**: Basic health check to confirm the service is running.
- **Response**:

```json
{
  "status": "success",
  "message": "Service is running"
}
```

---

### 2. `/api/create-user`

- **Method**: `POST` or `PUT`
- **Purpose**: Create a new user account.
- **Request Body**:

```json
{
  "username": "testuser",
  "password": "mypassword"
}
```

- **Response**:

```json
{
  "status": "success",
  "message": "User 'testuser' created successfully"
}
```

---

### 3. `/api/login`

- **Method**: `POST`
- **Purpose**: Log in a user.
- **Request Body**:

```json
{
  "username": "testuser",
  "password": "mypassword"
}
```

- **Response**:

```json
{
  "status": "success",
  "message": "User 'testuser' logged in successfully"
}
```

---

### 4. `/api/logout`

- **Method**: `POST`
- **Purpose**: Log out the current user.
- **Auth Required**: ✅
- **Response**:

```json
{
  "status": "success",
  "message": "User logged out successfully"
}
```

---

### 5. `/api/change-password`

- **Method**: `POST`
- **Purpose**: Change the password of the current user.
- **Auth Required**: ✅
- **Request Body**:

```json
{
  "new_password": "newsecurepassword"
}
```

- **Response**:

```json
{
  "status": "success",
  "message": "Password changed successfully"
}
```

---

### 6. `/api/pets` (GET)

- **Method**: `GET`
- **Purpose**: Get a list of all pets.
- **Response**:

```json
[
  {
    "id": 1,
    "name": "Charlie",
    "age": 3,
    "breed": "beagle",
    "weight": 25.0,
    "kid_friendly": true,
    "price": 300.0,
    "size": "medium",
    "image": "https://images.dog.ceo/breeds/beagle/n02088364_12345.jpg"
  }
]
```

---

### 7. `/api/pets` (POST)

- **Method**: `POST`
- **Purpose**: Add a new pet to the database.
- **Request Body**:

```json
{
  "name": "Charlie",
  "age": 3,
  "breed": "beagle",
  "weight": 25,
  "kid_friendly": true,
  "price": 300
}
```

- **Response**:

```json
{
  "status": "success",
  "message": "Pet added successfully"
}
```

---

### 8. `/api/get-pet-by-id/<int:pet_id>`

- **Method**: `GET`
- **Purpose**: Retrieve details for a specific pet by ID.
- **Response**:

```json
{
  "id": 1,
  "name": "Charlie",
  "age": 3,
  "breed": "beagle",
  "weight": 25.0,
  "kid_friendly": true,
  "price": 300.0,
  "size": "medium",
  "image": "https://images.dog.ceo/breeds/beagle/n02088364_12345.jpg"
}
```

---

### 9. `/api/delete-pet/<int:pet_id>`

- **Method**: `DELETE`
- **Purpose**: Delete a pet by its ID.
- **Response**:

```json
{
  "status": "success",
  "message": "Pet with ID 1 deleted successfully"
}
```

---

### 10. `/api/update-price/<int:pet_id>/price`

- **Method**: `PUT`
- **Purpose**: Update the price of a pet.
- **Request Body**:

```json
{
  "new_price": 350
}
```

- **Response**:

```json
{
  "status": "success",
  "message": "Price for pet with ID 1 updated successfully"
}
```

---

### 11. `/api/dog_photo`

- **Method**: `GET`
- **Purpose**: Fetch a dog photo based on breed.
- **Query Parameter**: `breed` (e.g., `beagle`, `basset/hound`)
- **Example**:

```
GET /api/dog_photo?breed=golden/retriever
```

- **Response**:

```json
{
  "status": "success",
  "breed": "golden/retriever",
  "photo_url": "https://images.dog.ceo/breeds/retriever-golden/n02099601_1234.jpg"
}
```

---

## 📁 Folder Structure

```
.
├── app.py
├── config.py
├── pets/
│   ├── db.py
│   ├── models/
│   ├── utils/
├── tests/
├── run_docker.sh
```
