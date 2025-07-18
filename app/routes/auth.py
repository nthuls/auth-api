# app/routes/auth.py
from flask import request
from flask_restx import Namespace, Resource, fields
import jwt
import datetime
from app import db, limiter
from app.models.user import User
from app.config import Config
from app.utils.validators import validate_email, validate_password_strength

auth_ns = Namespace('auth', description='Authentication operations')

# Request models
register_model = auth_ns.model('RegisterModel', {
    'email': fields.String(required=True, description='User email address'),
    'password': fields.String(required=True, description='User password')
})

login_model = auth_ns.model('LoginModel', {
    'email': fields.String(required=True, description='User email address'),
    'password': fields.String(required=True, description='User password')
})

# Response models
success_model = auth_ns.model('SuccessModel', {
    'message': fields.String(description='Success message')
})

token_model = auth_ns.model('TokenModel', {
    'token': fields.String(description='JWT token'),
    'expires_at': fields.DateTime(description='Token expiration time')
})

@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(register_model)
    @auth_ns.response(201, 'User successfully registered', success_model)
    @auth_ns.response(400, 'Validation error')
    @auth_ns.response(409, 'Email already registered')
    def post(self):
        data = request.json
        
        # Validate required fields
        if not data or not data.get('email') or not data.get('password'):
            return {'message': 'Email and password are required'}, 400
        
        # Validate email format
        if not validate_email(data.get('email')):
            return {'message': 'Invalid email format'}, 400
        
        # Validate password strength
        is_valid, message = validate_password_strength(data.get('password'))
        if not is_valid:
            return {'message': message}, 400
        
        # Check if user already exists
        if User.query.filter_by(email=data.get('email')).first():
            return {'message': 'Email already registered'}, 409
        
        # Create new user
        user = User(email=data.get('email'))
        user.password = data.get('password')
        
        db.session.add(user)
        db.session.commit()
        
        return {'message': 'User registered successfully'}, 201

@auth_ns.route('/login')
class Login(Resource):
    @limiter.limit("5 per minute")
    @auth_ns.expect(login_model)
    @auth_ns.response(200, 'Login successful', token_model)
    @auth_ns.response(401, 'Invalid credentials')
    def post(self):
        data = request.json
        
        # Validate required fields
        if not data or not data.get('email') or not data.get('password'):
            return {'message': 'Email and password are required'}, 400
        
        # Find the user
        user = User.query.filter_by(email=data.get('email')).first()
        
        # Check if user exists and password is correct
        if not user or not user.verify_password(data.get('password')):
            return {'message': 'Invalid credentials'}, 401
        
        # Generate expiration time
        exp_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=Config.JWT_EXPIRATION_DELTA)
        
        # Generate JWT token
        token = jwt.encode(
            {
                'sub': user.id,
                'email': user.email,
                'iat': datetime.datetime.now(datetime.UTC),
                'exp': exp_time
            },
            Config.JWT_SECRET_KEY,
            algorithm='HS256'
        )
        
        return {
            'token': token,
            'expires_at': exp_time.isoformat()
        }, 200