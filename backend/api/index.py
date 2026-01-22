from flask import Flask, jsonify, request
from flask_cors import CORS
from api.gemini import call_gemini

app = Flask(__name__)

# Configure CORS with proper settings for Vercel deployment
CORS(app,
     origins=[
         "http://localhost:5173",         # local dev
         "https://richwellp.github.io"
     ],
     methods=["GET", "POST", "OPTIONS"],
     allow_headers=["Content-Type"],
     supports_credentials=True)

@app.get("/")
def root():
    return jsonify(message="Hello from Flask on Vercel (hello.py)!")

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