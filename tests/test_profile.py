import pytest
import json
import jwt
import datetime
from app import create_app, db
from app.models.user import User
from app.config import Config

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            
            # Create test user
            user = User(email='test@example.com')
            user.password = 'Password123!'
            db.session.add(user)
            db.session.commit()
            
            yield client
            
            db.session.remove()
            db.drop_all()

@pytest.fixture
def auth_token(client):
    """Generate a valid auth token for the test user"""
    with client.application.app_context():
        user = User.query.filter_by(email='test@example.com').first()
        
        token = jwt.encode(
            {
                'sub': user.id,
                'email': user.email,
                'iat': datetime.datetime.now(datetime.UTC),
                'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
            },
            Config.JWT_SECRET_KEY,
            algorithm='HS256'
        )
        
        return token

def test_profile_with_valid_token(client, auth_token):
    """Test accessing profile with valid token"""
    response = client.get(
        '/profile/profile',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 200
    assert b'Welcome, test@example.com!' in response.data

def test_profile_without_token(client):
    """Test accessing profile without token"""
    response = client.get('/profile/profile')
    assert response.status_code == 401
    assert b'Authentication required' in response.data

def test_profile_with_invalid_token(client):
    """Test accessing profile with invalid token"""
    response = client.get(
        '/profile/profile',
        headers={'Authorization': 'Bearer invalid.token.here'}
    )
    assert response.status_code == 401
    assert b'Invalid token' in response.data