from flask import Flask, jsonify, request, Response, stream_with_context
from flask_cors import CORS
from flask_compress import Compress
from collections import defaultdict
from datetime import datetime, timedelta
import os
import json
from config import RATE_LIMIT_REQUESTS, RATE_LIMIT_WINDOW, MESSAGE_LENGTH_LIMIT, HISTORY_LIMIT, get_contact_message

app = Flask(__name__)

# Enable gzip compression for all responses
Compress(app)

# Register blueprints
from api.blog import blog_bp
from api.admin_blog import admin_blog_bp
from api.albums import albums_bp
from api.auth import auth_bp
from api.sitemap import sitemap_bp
app.register_blueprint(blog_bp, url_prefix='/blog')
app.register_blueprint(admin_blog_bp, url_prefix='/admin/blog')
app.register_blueprint(albums_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(sitemap_bp)

# CORS configuration for cross-origin requests
allowed_origins = os.environ.get('ALLOWED_ORIGINS', 'http://localhost:5173,https://richwellp.github.io,https://richwellp-github-io.vercel.app').split(',')
CORS(app,
     origins=allowed_origins,
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     supports_credentials=True,  # Allow credentials (not required for Bearer tokens, but harmless)
     allow_headers=['Content-Type', 'Authorization'])

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
    """Streaming chat endpoint using Server-Sent Events (SSE)"""
    if request.method == "OPTIONS":
        return "", 200

    import time
    import sys
    request_start = time.time()
    print(f"\n[Endpoint] ===== CHAT REQUEST RECEIVED at {time.strftime('%H:%M:%S')} =====", file=sys.stderr, flush=True)

    # Rate limiting
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if not check_rate_limit(client_ip):
        return jsonify(
            error="Too many requests. Please wait a moment before trying again.",
            error_type="rate_limit",
            message="Too many requests. Please wait a moment before trying again."
        ), 429

    try:
        from api.gemini import call_gemini_stream

        parse_start = time.time()
        data = request.get_json()
        parse_time = time.time() - parse_start
        print(f"[Endpoint] Request parsing took {parse_time:.3f}s", file=sys.stderr, flush=True)
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
            stream_start = time.time()
            try:
                for chunk in call_gemini_stream(user_message, history, site_context):
                    # Format as SSE
                    yield f"data: {json.dumps(chunk)}\n\n"

                # Send done signal with timing
                total_time = time.time() - request_start
                yield f"data: {json.dumps({'done': True, 'timing': {'total': round(total_time, 2), 'stream': round(time.time() - stream_start, 2)}})}\n\n"
            except Exception as e:
                print(f"Streaming error: {str(e)}", file=sys.stderr, flush=True)
                yield f"data: {json.dumps({'error': True, 'message': f'The AI is taking too long to respond. Please try again. {get_contact_message()}'})}\n\n"

        response = Response(
            stream_with_context(generate()),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no',
                'Connection': 'keep-alive',
                'X-Request-Start': str(request_start)
            }
        )

        print(f"[Endpoint] Returning response (setup took {time.time() - request_start:.2f}s)", file=sys.stderr, flush=True)
        return response

    except Exception as e:
        print(f"Chat error: {str(e)}")
        return jsonify(
            error="Failed to start chat",
            error_type="server_error",
            error_details=str(e),
            response=f"I'm having trouble right now. {get_contact_message()}"
        ), 500
