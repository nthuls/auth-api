from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address)

# Define authorization scheme for Swagger UI
authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Type in the *\'Value\'* input box below: **Bearer &lt;JWT&gt;**',
        'prefix': 'Bearer '
    }
}

# Initialize API with Swagger documentation
api = Api(
    version='1.0', 
    title='Authentication API',
    description='A simple authentication API with user registration and login',
    doc='/api/docs',
    authorizations=authorizations,
    security='Bearer Auth'
)

def create_app(config_name=None):
    app = Flask(__name__, instance_relative_config=True)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Load configuration
    app.config.from_object('app.config.Config')
    
    # Initialize extensions with app
    db.init_app(app)
    CORS(app)
    limiter.init_app(app)
    api.init_app(app)
    
    # Add security headers
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.redoc.ly; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; img-src 'self' data:; font-src 'self' data: https://fonts.gstatic.com; connect-src 'self'"
        return response
    
    # Import and register namespaces
    from app.routes.auth import auth_ns
    from app.routes.profile import profile_ns
    
    api.add_namespace(auth_ns)
    api.add_namespace(profile_ns)
    
    # Add ReDoc UI route
    @app.route('/api/redoc')
    def redoc():
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Authentication API - ReDoc</title>
            <meta charset="utf-8"/>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
            <style>
                body {
                    margin: 0;
                    padding: 0;
                }
            </style>
        </head>
        <body>
            <redoc spec-url='/api/swagger.json'></redoc>
            <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
        </body>
        </html>
        """
    
    # Add home page
    @app.route('/')
    def index():
        return """
        <html>
        <head>
            <title>Authentication API</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    line-height: 1.6;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                }
                h1 {
                    color: #333;
                }
                .docs-link {
                    margin: 20px 0;
                }
                .docs-link a {
                    display: inline-block;
                    margin-right: 20px;
                    padding: 10px 15px;
                    background-color: #4CAF50;
                    color: white;
                    text-decoration: none;
                    border-radius: 4px;
                }
                .docs-link a:hover {
                    background-color: #45a049;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Authentication API</h1>
                <p>Welcome to the Authentication API. This API provides endpoints for user registration, login, and profile management.</p>
                <div class="docs-link">
                    <a href="/api/docs">Swagger UI Documentation</a>
                    <a href="/api/redoc">ReDoc Documentation</a>
                </div>
            </div>
        </body>
        </html>
        """
    
    # Create database tables within app context
    with app.app_context():
        db.create_all()
    
    return app