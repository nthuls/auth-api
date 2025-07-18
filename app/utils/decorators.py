# app/utils/decorators.py

from functools import wraps
from flask import request, jsonify
from app.utils.auth_utils import get_user_from_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return {'message': 'Authentication required'}, 401
        
        try:
            payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(payload['sub'])
            
            if not current_user:
                return {'message': 'Invalid token'}, 401
                
        except jwt.ExpiredSignatureError:
            return {'message': 'Token has expired'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Invalid token'}, 401
            
        return f(current_user=current_user, *args, **kwargs)
    
    return decorated