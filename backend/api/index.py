from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def root():
    return jsonify(message="Hello from Flask on Vercel!")

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return "", 200

    try:
        from api.gemini import call_gemini

        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify(error="Message is required"), 400

        user_message = data.get('message', '').strip()
        if not user_message:
            return jsonify(error="Message cannot be empty"), 400

        history = data.get('history', [])
        site_context = data.get('site_context', {})

        response_text = call_gemini(user_message, history, site_context)
        return jsonify(response=response_text)

    except Exception as e:
        print(f"Chat error: {str(e)}")
        return jsonify(
            error="An error occurred",
            response="I'm having trouble right now. Please contact richwell.perez@gmail.com directly."
        ), 500
