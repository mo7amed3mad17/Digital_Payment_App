
# Simple Payments App

## Overview

**Simple Payments** is a streamlined financial application designed to simplify peer-to-peer money transfers while maintaining robust security. Users can manage their transactions, track payment history, and connect with other users through unique account numbers.

## Features

- **User registration** with automatic account creation.
- **Account number generation** based on the user's ID.
- **Transfer of funds** between registered users.
- **Bill payments and mobile balance top-ups** (planned for future versions).
- **Transaction History**: Users can view a list of their past transactions, including sent and received amounts.
- **Simple and Secure Interface**: The app features an intuitive interface with basic security features like authentication via **JWT (JSON Web Tokens)** for encrypted data transmission.

## Architecture

The app is built using **Flask** as the web framework, **Gunicorn** as the WSGI server for production deployment, and **PostgreSQL** as the database for storing user and transaction data. The app is deployed on **Render.com** for easy cloud hosting.

The project includes the following main components:
- **User Model**: Stores user data such as username, password, etc.
- **Account Model**: Each user has an associated account containing their account number and balance.
- **Transaction Model**: Stores details of money transfers between users, including sender and receiver details and the transaction amount.

The app uses **Flask** to handle HTTP requests and responses, with **Gunicorn** serving the application in production. The database is managed using **PostgreSQL**, and the application is deployed on **Render.com** to provide a scalable cloud hosting solution.

## Technologies Used

- **Backend Framework**: Flask
- **Database**: PostgreSQL
- **Security**: JWT for user authentication
- **Frontend**: HTML/CSS for simple front-end development
- **Testing**: Postman for testing API endpoints

## Setup Instructions

### Prerequisites

- Python 3.x
- PostgreSQL

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/mo7amed3mad17/Digital_Payment_App.git
    ```

2. Navigate to the project directory:

    ```bash
    cd payment-app
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:

    ```bash
    python3 run.py
    ```

## API Documentation

### Base URL
`http://digital-payment-app.onrender.com/api/v1/`

### Authentication
All endpoints require **Bearer Authentication**. Include your **JWT token** in the `Authorization` header as `Bearer <your_access_token>`.

---

### 1. **POST /register**
Registers a new user and automatically creates an associated account.

#### Request Body Example:
```json
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "phone_number": "1234567890",
  "password": "securepassword"
}
```

#### Possible Responses:
- **201 Created**: User and account created successfully.
  ```json
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
  ```
- **400 Bad Request**: Missing required fields.
  ```json
  {
    "error": "Missing required fields"
  }
  ```
- **500 Internal Server Error**: Server error (e.g., database issue).
  ```json
  {
    "error": "Description of the error"
  }
  ```

---

### 2. **POST /login**
Authenticates a user and returns a JWT for session management.

#### Request Body Example:
```json
{
  "username": "johndoe",
  "password": "securepassword"
}
```

#### Possible Responses:
- **200 OK**: User authenticated, JWT provided.
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```
- **401 Unauthorized**: Invalid username or password.
  ```json
  {
    "error": "Invalid username or password"
  }
  ```

---

### 3. **GET /users/me**
Returns the authenticated user's username and ID.

#### Request Header:
```http
Authorization: Bearer <access_token>
```

#### Possible Responses:
- **200 OK**: Successfully retrieved user details.
  ```json
  {
    "id": 1,
    "username": "johndoe"
  }
  ```
- **404 Not Found**: User not found.
  ```json
  {
    "msg": "User not found"
  }
  ```
- **401 Unauthorized**: Missing or invalid JWT token.

---

### 4. **GET /users/{user_id}**
Returns detailed information about a specific user, including account details.

#### Request Header:
```http
Authorization: Bearer <access_token>
```

#### Possible Responses:
- **200 OK**: Successfully retrieved user and account details.
  ```json
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
  ```
- **404 Not Found**: User or account not found.
  ```json
  {
    "error": "User not found"
  }
  ```
- **401 Unauthorized**: Missing or invalid JWT token.

---

### 5. **GET /transactions/{user_id}**
Returns the transaction history for a specific user.

#### Request Header:
```http
Authorization: Bearer <access_token>
```

#### Possible Responses:
- **200 OK**: Successfully retrieved transaction history.
  ```json
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
  ```
- **404 Not Found**: User not found.
  ```json
  {
    "error": "User not found"
  }
  ```
- **401 Unauthorized**: Missing or invalid JWT token.

---

## Graduation Project Note

This project is designed as a **graduation project** for a software engineering course and is not intended to integrate with real-world banking APIs at this stage. The goal is to provide a working prototype of a digital payment application, focusing on the basic functionality simulating peer-to-peer transactions.