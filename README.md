# Authentication API

A robust and secure authentication API built with Flask and SQLite that supports user registration and login using email and password. This project was created for Backend Hackathon Challenge 3.

## Features

- User Registration with email and password
- User Login with JWT token authentication
- Protected Routes requiring authentication
- Secure password hashing
- Email format validation
- Token expiration (1 hour)

### Security Features

- Password hashing with bcrypt
- JWT with expiration
- Rate limiting for login attempts
- CORS protection
- Environment variables for secrets
- Request validation
- XSS protection headers
- SQL injection protection (via SQLAlchemy)

## Project Structure

```
auth-api/
├── .env                    # Environment variables
├── .gitignore              # Git ignore file
├── README.md               # Project documentation
├── requirements.txt        # Project dependencies
├── run.py                  # Application entry point
├── instance/               # Instance-specific data
│   └── auth.db             # SQLite database
├── app/                    # Application package
│   ├── __init__.py         # Initialize Flask app
│   ├── config.py           # Configuration settings
│   ├── models/             # Database models
│   │   ├── __init__.py
│   │   └── user.py         # User model
│   ├── routes/             # API routes
│   │   ├── __init__.py
│   │   ├── auth.py         # Authentication routes
│   │   └── profile.py      # Profile routes
│   └── utils/              # Utility modules
│       ├── __init__.py
│       ├── auth_utils.py   # Authentication utilities
│       ├── decorators.py   # Custom decorators
│       └── validators.py   # Input validators
└── tests/                  # Unit and integration tests
    ├── __init__.py
    ├── test_auth.py
    └── test_profile.py
```

## Technical Stack

- **Framework**: Flask
- **Database**: SQLite with Flask-SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens)
- **Documentation**: Swagger UI and ReDoc via Flask-RESTX
- **Security**: Flask-Limiter, Flask-Cors, bcrypt

## API Endpoints

### 1. User Registration
- **Endpoint**: `POST /api/register`
- **Description**: Register a new user
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securePassword123"
  }
  ```
- **Response**: 201 Created
  ```json
  {
    "message": "User registered successfully"
  }
  ```

### 2. User Login
- **Endpoint**: `POST /api/login`
- **Description**: Authenticate a user and get a token
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securePassword123"
  }
  ```
- **Response**: 200 OK
  ```json
  {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_at": "2025-07-18T15:30:00Z"
  }
  ```

### 3. Get User Profile
- **Endpoint**: `GET /api/profile`
- **Description**: Get the authenticated user's profile
- **Headers**: `Authorization: Bearer <token>`
- **Response**: 200 OK
  ```json
  {
    "message": "Welcome, user@example.com!"
  }
  ```

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root with the following variables:
   ```
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your_super_secret_key
   JWT_SECRET_KEY=your_jwt_secret_key
   ```
5. Initialize the database:
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```
6. Run the application:
   ```
   flask run
   ```
7. Access the API documentation:
   - Swagger UI: http://localhost:5000/api/docs
   - ReDoc: http://localhost:5000/api/redoc

## Testing

Run tests using pytest:
```
pytest
```

## Future Improvements

- Password reset functionality
- Email verification
- Two-factor authentication
- OAuth integration
- Role-based access control