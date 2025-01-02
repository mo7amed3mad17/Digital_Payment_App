Simple Payments App
A secure and user-friendly digital payment application focusing on peer-to-peer transactions.

Overview:
Simple Payments is a streamlined financial application designed to simplify peer-to-peer money transfers while maintaining robust security. Users can manage their transactions, track payment history, and connect with other users through unique account numbers.

Features:
User registration with automatic account creation.
Account number generation based on the user's ID.
Transfer of funds between registered users.
Bill payments and mobile balance top-ups (planned for future versions).
Transaction History: Users can view a list of their past transactions, including sent and received amounts.
Simple and Secure Interface: The app will feature a simple, intuitive interface with basic security features such as authentication via JWT (JSON Web Tokens) allowing encrypted data transmission.

Architecture:
The app is built using Flask as the web framework, Gunicorn as the WSGI server for production deployment, and SQLite as the database for storing user and transaction data. The app is deployed on Render.com for easy cloud hosting.

The project includes the following main components:

User Model: Stores user data such as username, password, etc.
Account Model: Each user has an associated account containing their account number and balance.
Transaction Model: Stores the details of money transfers between users, including sender and receiver details, and the transaction amount.
The app uses Flask to handle HTTP requests and responses, with Gunicorn serving the application in a production environment. The database is managed using SQLite, and the application is deployed on Render.com to provide a scalable cloud hosting solution.

Technologies Used:
Backend Framework: Flask, SQLAlchemy
Database: SQLite
Security: JWT for user authentication
Frontend: HTML/CSS for simple front-end development.
Testing: Postman was used for testing API endpoints.

Setup Instructions:
Prerequisites:
Python 3.x
SQLite3

Installation:
Clone the repository:
e
git clone https://github.com/mo7amed3mad17/Digital_Payment_App.git
Navigate to the project directory:
cd payment-app
Install the required dependencies:
pip install -r requirements.txt

Usage:
run the application using:
python3 run.py

API Documentation:-
Base URL ---> http://digital-payment-app.onrender.com/api/v1/
Authentication ----> Authorization: Bearer <your_access_token>

Endpoints:
1- The Endpoint: POST /register
Description: Registers a new user and automatically creates an associated account.
Request Body Example:
{
    "username": "johndoe",
    "email": "johndoe@example.com",
    "phone_number": "1234567890",
    "password": "securepassword"
}

Potential Responses:
a- 201 Created:
The user and account were successfully created.
Response Body:
{
    "message": "User and account registered successfully",
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "johndoe@example.com"
    },
    "account": {
        "id": 1,
        "account_number": "2003622",
        "balance": 0.0
    }
}

b- 400 Bad Request:
Missing required fields.
Response Body:
{
    "error": "Missing required fields"
}

c- 500 Internal Server Error:
A server error occurred, such as a database issue.
Response Body:
{
    "error": "Description of the error"
}

2- The Endpoint: POST /login
Description: Authenticates a user by verifying their credentials and returns a JSON Web Token (JWT) for session management.
Request Body Example:
{
    "username": "johndoe",
    "password": "securepassword"
}

Potetial Responses:
a- 200 OK:
The user is successfully authenticated, and a JWT is provided for further requests.
Response Body:
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

b- 401 Unauthorized:
Invalid username or password.
Response Body:
{
    "error": "Invalid username or password"
}

3- The Endpoint : GET /users/me
Description: Return Username and ID, which can be used to get the user inforation.
Request Body Example:
GET /users/me HTTP/1.1
Host: http://digital-payment-app.onrender.com/
Authorization: Bearer <access_token>

Potebtial Responses:
a- 200 OK:
Successfully retrieved the authenticated user's details.
{
    "id": 1,
    "username": "johndoe"
}

b- 404 Not Found:
The user associated with the provided token does not exist.
Response Body:
{
    "msg": "User not found"
}

c- 401 Unauthorized:
Missing or invalid JWT token.

4- The Endpoint : GET /users/<int:user_id>
Description: Retrieves detailed information about a specific user, including their associated account details.
Parameter: <user_id> is unique identifier gotten from the previous route /users/me. 
Request Body Example:
GET /users/1 HTTP/1.1
Host: http://digital-payment-app.onrender.com
Authorization: Bearer <access_token>

Potebtial Responses:
a- 200 OK:
Successfully retrieved the user's details and account information.
Response Body:
{
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "johndoe@example.com",
        "phone_number": "123456789"
    },
    "account": {
        "account_number": "2003622",
        "balance": 1000.0,
        "created_at": "2025-01-01T12:00:00"
    }
}

b- 404 Not Found:
If the user does not exist:
Response Body:
{
    "error": "User not found"
}
If the account does not exist for the given user:
Response Body:
{
    "error": "Account not found"
}

c- 401 Unauthorized:
Missing or invalid JWT token.


5- The Endpoint : GET /transactions/<int:user_id>
Description: Return User transactions.
Parameter: <user_id> is unique identifier gotten from the previous route /users/me.
Request Body Example:
GET /transactions/1 HTTP/1.1
Host: http://digital-payment-app.onrender.com
Authorization: Bearer <access_token>

Potebtial Responses:
a- 200 OK:
Successfully retrieved the transaction history for the specified user.
Response Body:
{
    "sent": [
        {
            "id": 1,
            "amount": 500.0,
            "to": "2003622",
            "datetime": "2025-01-01T10:00:00"
        },
        {
            "id": 2,
            "amount": 250.0,
            "to": "2003623",
            "datetime": "2025-01-02T15:30:00"
        }
    ],
    "received": [
        {
            "id": 3,
            "amount": 1000.0,
            "from": "2003624",
            "datetime": "2025-01-03T09:45:00"
        }
    ]
}

b- 404 Not Found:
If the user does not exist:
Response Body:
{
    "error": "User not found"
}

c- 401 Unauthorized:
Missing or invalid JWT token.


This project is designed as a graduation project for a software engineering course and is not intended to integrate with real-world banking APIs at this stage. The goal is to provide a working prototype of a digital payment application, focusing on the basic functionality simulating peer-to-peer transactions.