"""
Authentication API endpoints
Provides login/logout/status endpoints for Bearer token authentication
"""
from flask import Blueprint, request, jsonify
from auth import (
    verify_admin_key,
    get_auth_status,
    require_admin
)

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """
    POST /auth/login
    Body: { "key": "admin_key_here" }

    Verifies admin key. Frontend stores in localStorage and sends as Bearer token.

    Returns:
        200: Key is valid (frontend will store it)
        400: Missing key
        401: Invalid key
    """
    data = request.get_json()

    if not data or 'key' not in data:
        return jsonify(error='Admin key required'), 400

    key = data.get('key', '').strip()

    if not verify_admin_key(key):
        return jsonify(error='Invalid admin key'), 401

    return jsonify({
        'message': 'Login successful',
        'authenticated': True,
        'method': 'bearer'
    })


@auth_bp.route('/auth/logout', methods=['POST'])
def logout():
    """
    POST /auth/logout

    No-op endpoint. Frontend clears localStorage on logout.

    Returns:
        200: Logout acknowledged
    """
    return jsonify({
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
