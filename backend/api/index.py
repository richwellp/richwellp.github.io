from flask import Flask, jsonify, request, Response, stream_with_context
from flask_cors import CORS
from collections import defaultdict
from datetime import datetime, timedelta
import os
import json
from config import RATE_LIMIT_REQUESTS, RATE_LIMIT_WINDOW, MESSAGE_LENGTH_LIMIT, HISTORY_LIMIT, get_contact_message

app = Flask(__name__)

# Register blueprints
from api.blog import blog_bp
from api.albums import albums_bp
app.register_blueprint(blog_bp, url_prefix='/blog')
app.register_blueprint(albums_bp)

# Secure CORS configuration
allowed_origins = os.environ.get('ALLOWED_ORIGINS', 'http://localhost:*,https://richwellp.github.io,https://*.vercel.app').split(',')
CORS(app, origins=allowed_origins, methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

# Simple in-memory rate limiter (per IP)
rate_limit_storage = defaultdict(list)

@app.route("/", methods=["GET"])
def root():
    return jsonify(message="Hello from Flask on Vercel!")

def check_rate_limit(ip_address):
    """Check if IP has exceeded rate limit."""
    now = datetime.now()
    cutoff = now - timedelta(seconds=RATE_LIMIT_WINDOW)

    # Clean old entries
    rate_limit_storage[ip_address] = [
        timestamp for timestamp in rate_limit_storage[ip_address]
        if timestamp > cutoff
    ]

    # Check if exceeded
    if len(rate_limit_storage[ip_address]) >= RATE_LIMIT_REQUESTS:
        return False

    # Add current request
    rate_limit_storage[ip_address].append(now)
    return True


@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return "", 200

    # Rate limiting
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if not check_rate_limit(client_ip):
        return jsonify(
            error="Too many requests. Please wait a moment before trying again.",
            error_type="rate_limit",
            message="Too many requests. Please wait a moment before trying again."
        ), 429

    try:
        from api.gemini import call_gemini

        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify(
                error="Message is required",
                error_type="validation_error"
            ), 400

        user_message = data.get('message', '').strip()
        if not user_message:
            return jsonify(
                error="Message cannot be empty",
                error_type="validation_error"
            ), 400

        # Validate message length
        if len(user_message) > MESSAGE_LENGTH_LIMIT:
            return jsonify(
                error=f"Message is too long. Please keep it under {MESSAGE_LENGTH_LIMIT} characters.",
                error_type="validation_error"
            ), 400

        history = data.get('history', [])
        site_context = data.get('site_context', {})

        # Validate and limit history size
        if not isinstance(history, list):
            history = []
        # Limit to last 20 messages to prevent context overflow
        history = history[-HISTORY_LIMIT:]

        response_text = call_gemini(user_message, history, site_context)

        # Check if response is an error dictionary
        if isinstance(response_text, dict) and response_text.get('error'):
            error_type = response_text.get('error_type', 'api_error')
            status_code = 429 if error_type == 'rate_limit' else 500

            print(f"Gemini returned error: {error_type} - {response_text.get('details', 'No details')}")

            return jsonify(
                error=response_text.get('message', 'An error occurred'),
                error_type=error_type,
                error_details=response_text.get('details'),
                response=response_text.get('message')  # For backward compatibility
            ), status_code

        return jsonify(response=response_text)

    except Exception as e:
        print(f"Chat error: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return jsonify(
            error="An error occurred",
            error_type="server_error",
            error_details=str(e),
            response=f"I'm having trouble right now. {get_contact_message()}"
        ), 500


@app.route("/chat/stream", methods=["POST", "OPTIONS"])
def chat_stream():
    """Streaming endpoint using Server-Sent Events (SSE)"""
    if request.method == "OPTIONS":
        return "", 200

    # Rate limiting
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if not check_rate_limit(client_ip):
        return jsonify(
            error="Too many requests. Please wait a moment before trying again.",
            error_type="rate_limit",
            message="Too many requests. Please wait a moment, or contact Richwell directly at richwell.perez@gmail.com."
        ), 429

    try:
        from api.gemini import call_gemini_stream

        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify(
                error="Message is required",
                error_type="validation_error"
            ), 400

        user_message = data.get('message', '').strip()
        if not user_message:
            return jsonify(
                error="Message cannot be empty",
                error_type="validation_error"
            ), 400

        # Validate message length
        if len(user_message) > MESSAGE_LENGTH_LIMIT:
            return jsonify(
                error=f"Message is too long. Please keep it under {MESSAGE_LENGTH_LIMIT} characters.",
                error_type="validation_error"
            ), 400

        history = data.get('history', [])
        site_context = data.get('site_context', {})

        # Validate and limit history size
        if not isinstance(history, list):
            history = []
        history = history[-HISTORY_LIMIT:]

        def generate():
            """Generator function for SSE"""
            try:
                for chunk in call_gemini_stream(user_message, history, site_context):
                    # Format as SSE
                    yield f"data: {json.dumps(chunk)}\n\n"

                # Send done signal
                yield f"data: {json.dumps({'done': True})}\n\n"
            except Exception as e:
                print(f"Streaming error: {str(e)}")
                yield f"data: {json.dumps({'error': True, 'message': 'Streaming interrupted. Please contact Richwell at richwell.perez@gmail.com.'})}\n\n"

        return Response(
            stream_with_context(generate()),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no',
                'Connection': 'keep-alive'
            }
        )

    except Exception as e:
        print(f"Stream setup error: {str(e)}")
        return jsonify(
            error="Failed to start streaming",
            error_type="server_error",
            error_details=str(e),
            response=f"I'm having trouble right now. {get_contact_message()}"
        ), 500
