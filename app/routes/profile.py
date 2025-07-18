# app/routes/profile.py

from flask import request
from flask_restx import Namespace, Resource, fields
from app.utils.decorators import token_required

profile_ns = Namespace('profile', description='User profile operations')

# Response models
profile_model = profile_ns.model('ProfileModel', {
    'message': fields.String(description='Welcome message')
})

@profile_ns.route('/profile')
class Profile(Resource):
    @profile_ns.doc(security='Bearer Auth')
    @profile_ns.response(200, 'Success', profile_model)
    @profile_ns.response(401, 'Authentication required')
    @token_required
    def get(self, current_user):
        return {'message': f'Welcome, {current_user.email}!'}, 200