для теста:

`uvicorn main:app 

// регистрация

curl -X POST "http://localhost:8000/auth/register"   -H "Content-Type: application/json"   -d '{
    "username": "DonaldTrump",
    "email": "dtrump@example.com",
    "password": "securepass123",
    "full_name": "Donald Vladimirovich Trump"
  }'

// логин

curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username_or_email": "joebiden@example.com", "password": "password123"}'

//

`


