# tests/test_auth.py

import pytest
import json
from app import create_app, db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_register(client):
    """Test user registration"""
    response = client.post(
        '/api/register',
        data=json.dumps({
            'email': 'test@example.com',
            'password': 'Password123!'
        }),
        content_type='application/json'
    )
    assert response.status_code == 201
    assert b'User registered successfully' in response.data

def test_register_duplicate_email(client):
    """Test registration with duplicate email"""
    # Register first user
    client.post(
        '/api/register',
        data=json.dumps({
            'email': 'test@example.com',
            'password': 'Password123!'
        }),
        content_type='application/json'
    )
    
    # Try to register with same email
    response = client.post(
        '/api/register',
        data=json.dumps({
            'email': 'test@example.com',
            'password': 'DifferentPass456!'
        }),
        content_type='application/json'
    )
    assert response.status_code == 409
    assert b'Email already registered' in response.data

def test_login(client):
    """Test user login"""
    # Register user
    client.post(
        '/api/register',
        data=json.dumps({
            'email': 'test@example.com',
            'password': 'Password123!'
        }),
        content_type='application/json'
    )
    
    # Login
    response = client.post(
        '/api/login',
        data=json.dumps({
            'email': 'test@example.com',
            'password': 'Password123!'
        }),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'token' in data
    assert 'expires_at' in data

def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    # Register user
    client.post(
        '/api/register',
        data=json.dumps({
            'email': 'test@example.com',
            'password': 'Password123!'
        }),
        content_type='application/json'
    )
    
    # Login with wrong password
    response = client.post(
        '/api/login',
        data=json.dumps({
            'email': 'test@example.com',
            'password': 'WrongPassword!'
        }),
        content_type='application/json'
    )
    assert response.status_code == 401
    assert b'Invalid credentials' in response.data