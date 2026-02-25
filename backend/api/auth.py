"""
Authentication API endpoints
Provides login/logout/status endpoints with secure httpOnly cookies
"""
from flask import Blueprint, request, jsonify
from auth import (
    verify_admin_key,
    create_admin_cookie_response,
    clear_admin_cookie_response,
    get_auth_status,
    require_admin
)

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """
    POST /auth/login
    Body: { "key": "admin_key_here" }

    Authenticates admin user and sets httpOnly secure cookie.

    Returns:
        200: Login successful, cookie set
        400: Missing key
        401: Invalid key
    """
    data = request.get_json()

    if not data or 'key' not in data:
        return jsonify(error='Admin key required'), 400

    key = data.get('key', '').strip()

    if not verify_admin_key(key):
        return jsonify(error='Invalid admin key'), 401

    # Create response with httpOnly cookie
    return create_admin_cookie_response({
        'message': 'Login successful',
        'authenticated': True,
        'method': 'cookie'
    })


@auth_bp.route('/auth/logout', methods=['POST'])
def logout():
    """
    POST /auth/logout

    Clears admin session cookie.

    Returns:
        200: Logout successful, cookie cleared
    """
    return clear_admin_cookie_response({
        'message': 'Logged out successfully',
        'authenticated': False
    })


@auth_bp.route('/auth/status', methods=['GET'])
def auth_status():
    """
    GET /auth/status

    Check current authentication status.

    Returns:
        200: Authentication status information
    """
    status = get_auth_status()
    return jsonify(status)


@auth_bp.route('/auth/verify', methods=['GET'])
@require_admin
def verify_auth():
    """
    GET /auth/verify

    Verify that the current session is authenticated.
    Protected endpoint that requires valid authentication.

    Returns:
        200: Authenticated
        401: Not authenticated
    """
    status = get_auth_status()
    return jsonify({
        'authenticated': True,
        'method': status['method'],
        'message': 'Authentication valid'
    })
