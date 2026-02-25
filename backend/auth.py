"""
Authentication utilities for admin endpoints
Uses Bearer token authentication with timing-safe comparison
"""
from functools import wraps
from flask import request, jsonify
import os
import secrets

ADMIN_KEY = os.getenv('BLOG_ADMIN_KEY')


def require_admin(f):
    """
    Decorator to require admin authentication via Bearer token.
    Expects: Authorization: Bearer <token> header
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', '')

        if not auth.startswith('Bearer '):
            return jsonify(error='Unauthorized'), 401

        token = auth[7:]  # Remove 'Bearer ' prefix

        if ADMIN_KEY and secrets.compare_digest(token, ADMIN_KEY):
            return f(*args, **kwargs)

        return jsonify(error='Unauthorized'), 401

    return decorated


def verify_admin_key(key):
    """
    Verify if the provided key matches the admin key.
    Uses constant-time comparison to prevent timing attacks.

    Args:
        key: Admin key to verify

    Returns:
        bool: True if valid, False otherwise
    """
    if not key or not ADMIN_KEY:
        return False

    # Use secrets.compare_digest for constant-time comparison (prevents timing attacks)
    return secrets.compare_digest(key.strip(), ADMIN_KEY)


def get_auth_status():
    """
    Check if the current request is authenticated via Bearer token.

    Returns:
        dict: Authentication status information
    """
    auth = request.headers.get('Authorization', '')

    if auth.startswith('Bearer ') and ADMIN_KEY:
        token = auth[7:]
        if secrets.compare_digest(token, ADMIN_KEY):
            return {
                'authenticated': True,
                'method': 'bearer'
            }

    return {
        'authenticated': False,
        'method': None
    }
