"""
Authentication utilities for admin endpoints
Supports both cookie-based (secure) and header-based (legacy) authentication
"""
from functools import wraps
from flask import request, jsonify, make_response
from datetime import datetime, timedelta
import os

ADMIN_KEY = os.getenv('BLOG_ADMIN_KEY')
COOKIE_NAME = 'admin_session'
COOKIE_MAX_AGE = 24 * 60 * 60  # 24 hours in seconds

# Detect if running in development mode
IS_PRODUCTION = os.getenv('FLASK_ENV') == 'production' or os.getenv('VERCEL_ENV') is not None


def require_admin(f):
    """
    Decorator to require admin authentication.
    Supports both:
    1. HttpOnly secure cookies (preferred)
    2. Authorization Bearer header (legacy, for backwards compatibility)
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Try cookie-based auth first (more secure)
        cookie_token = request.cookies.get(COOKIE_NAME)
        if cookie_token and cookie_token == ADMIN_KEY:
            return f(*args, **kwargs)

        # Fall back to header-based auth (legacy)
        auth = request.headers.get('Authorization', '')
        if auth.startswith('Bearer ') and auth[7:] == ADMIN_KEY:
            return f(*args, **kwargs)

        return jsonify(error='Unauthorized'), 401

    return decorated


def create_admin_cookie_response(data, status=200):
    """
    Create a response with admin session cookie set.

    Args:
        data: Response data (dict or string)
        status: HTTP status code

    Returns:
        Flask response with httpOnly secure cookie
    """
    response = make_response(jsonify(data) if isinstance(data, dict) else data, status)

    # Set httpOnly secure cookie
    response.set_cookie(
        COOKIE_NAME,
        value=ADMIN_KEY,
        max_age=COOKIE_MAX_AGE,
        secure=IS_PRODUCTION,  # Only sent over HTTPS in production
        httponly=True,  # Not accessible via JavaScript (prevents XSS)
        samesite='None' if IS_PRODUCTION else 'Lax'  # None required for cross-origin cookies in production
    )

    return response


def clear_admin_cookie_response(data=None, status=200):
    """
    Create a response that clears the admin session cookie.

    Args:
        data: Response data (dict or string)
        status: HTTP status code

    Returns:
        Flask response with cookie deletion
    """
    response = make_response(
        jsonify(data) if data and isinstance(data, dict) else jsonify(message='Logged out'),
        status
    )

    # Delete cookie
    response.set_cookie(
        COOKIE_NAME,
        value='',
        max_age=0,
        secure=IS_PRODUCTION,
        httponly=True,
        samesite='None' if IS_PRODUCTION else 'Lax'
    )

    return response


def verify_admin_key(key):
    """
    Verify if the provided key matches the admin key.

    Args:
        key: Admin key to verify

    Returns:
        bool: True if valid, False otherwise
    """
    if not key or not ADMIN_KEY:
        return False

    return key.strip() == ADMIN_KEY


def get_auth_status():
    """
    Check if the current request is authenticated.

    Returns:
        dict: Authentication status information
    """
    # Check cookie first
    cookie_token = request.cookies.get(COOKIE_NAME)
    if cookie_token and cookie_token == ADMIN_KEY:
        return {
            'authenticated': True,
            'method': 'cookie',
            'expires_in': COOKIE_MAX_AGE
        }

    # Check header
    auth = request.headers.get('Authorization', '')
    if auth.startswith('Bearer ') and auth[7:] == ADMIN_KEY:
        return {
            'authenticated': True,
            'method': 'bearer',
            'expires_in': None  # No expiration for bearer tokens
        }

    return {
        'authenticated': False,
        'method': None,
        'expires_in': None
    }
