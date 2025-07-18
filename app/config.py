# app/config.py

import os
from datetime import timedelta
import socket

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_dev_key')
    
    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'instance', 'auth.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'default_jwt_key')
    JWT_EXPIRATION_DELTA = int(os.environ.get('JWT_EXPIRATION_DELTA', 3600))  # 1 hour
    
    # Rate limiting
    RATELIMIT_DEFAULT = "200 per day, 50 per hour"
    RATELIMIT_STRATEGY = "fixed-window"
    
    # CORS configuration
    CORS_ORIGINS = ['*'] 

    # Cors allows all in development environment but we can uncomment below to allow specific ips

    # # Get the local IP address dynamically
    # LOCAL_IP = socket.gethostbyname(socket.gethostname())

    # # Add optional Tailscale IP manually if needed
    # TAILSCALE_IP = '100.x.x.x'  # Replace with your actual Tailscale IP

    # CORS_ORIGINS = [
    #     "http://localhost:3000",
    #     "http://127.0.0.1:3000",
    #     f"http://{LOCAL_IP}:3000",
    #     f"http://{TAILSCALE_IP}:3000"
    # ]  