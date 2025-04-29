#!/bin/bash

BASE_URL="http://localhost:5050/api"
USERNAME="testuser"
PASSWORD="password123"

echo "=== SMOKETEST: PET APP ==="

print_status() {
  if [ $1 -eq 0 ]; then
    echo "[PASS] $2"
  else
    echo "[FAIL] $2"
    exit 1
  fi
}

# Health check
echo "-> Checking service health..."
curl -s "$BASE_URL/health" | grep -q '"status": "success"'
print_status $? "Health check passed"

# Create user
echo "-> Creating user..."
curl -s -X POST "$BASE_URL/create-user" -H "Content-Type: application/json" -d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\"}" | grep -q '"status": "success"'
print_status $? "User creation passed"

# Login and save cookies
echo "-> Logging in..."
curl -s -c cookies.txt -X POST "$BASE_URL/login" -H "Content-Type: application/json" -d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\"}" | grep -q '"status": "success"'
print_status $? "Login passed"

# Add a pet
echo "-> Adding a pet..."
curl -s -b cookies.txt -X POST "$BASE_URL/add-pet" -H "Content-Type: application/json" -d '{
  "name": "Buddy",
  "age": 3,
  "breed": "Golden Retriever",
  "weight": 30,
  "kid_friendly": true,
  "price": 500
}' | grep -q '"status": "success"'
print_status $? "Pet addition passed"

# List pets
echo "-> Listing pets..."
curl -s "$BASE_URL/pets" | grep -q '"name": "Buddy"'
print_status $? "Pet listing passed"

# Get pet by ID 1 (assuming Buddy got ID=1)
echo "-> Getting pet by ID..."
curl -s "$BASE_URL/get-pet-by-id/1" | grep -q '"name": "Buddy"'
print_status $? "Get pet by ID passed"

# Update pet price
echo "-> Updating pet price..."
curl -s -b cookies.txt -X PUT "$BASE_URL/update-price/1/price" -H "Content-Type: application/json" -d '{"new_price": 550}' | grep -q '"status": "success"'
print_status $? "Update pet price passed"

# Delete pet
echo "-> Deleting pet..."
curl -s -b cookies.txt -X DELETE "$BASE_URL/delete-pet/1" | grep -q '"status": "success"'
print_status $? "Pet deletion passed"

echo "=== ALL SMOKETESTS PASSED SUCCESSFULLY ==="

# Cleanup
rm -f cookies.txt

