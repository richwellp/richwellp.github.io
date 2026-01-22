from flask import Flask, jsonify, request
from api.gemini import call_gemini

app = Flask(__name__)

# Manual CORS configuration for Vercel compatibility
@app.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    allowed_origins = [
        'http://localhost:5173',
        'https://richwellp.github.io'
    ]

    if origin in allowed_origins:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Credentials'] = 'true'

    return response

@app.get("/")
def root():
    return jsonify(message="Hello from Flask on Vercel (hello.py)!")

@app.route("/chat", methods=["OPTIONS"])
def chat_preflight():
    """Handle preflight OPTIONS request for /chat endpoint"""
    return "", 204

@app.post("/chat")
def chat():
    """
    Handle chat messages from the frontend.
    Expects JSON: {"message": "user message", "history": [{"role": "user"|"assistant", "content": "..."}]}
    Returns JSON: {"response": "assistant response"}
    """
    try:
        data = request.get_json()

        if not data or 'message' not in data:
            return jsonify(error="Message is required"), 400

        user_message = data.get('message', '').strip()
        if not user_message:
            return jsonify(error="Message cannot be empty"), 400

        history = data.get('history', [])
        site_context = data.get('site_context', {})

        # Call Gemini API with site context
        response_text = call_gemini(user_message, history, site_context)

        return jsonify(response=response_text)

    except Exception as e:
        print(f"Chat endpoint error: {str(e)}")
        return jsonify(
            error="An error occurred processing your request",
            response="I'm having trouble right now. Please contact richwell.perez@gmail.com directly."
        ), 500