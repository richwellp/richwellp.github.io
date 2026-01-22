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

        history = data.get('history', [])
        site_context = data.get('site_context', {})

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
            response="I'm having trouble right now. Please reach out directly at richwell.perez@gmail.com or linkedin.com/in/richwell-perez."
        ), 500
