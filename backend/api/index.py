from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    return jsonify(message="Hello from Flask on Vercel!")

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    """
    Handle chat messages from the frontend.
    OPTIONS method is for CORS preflight - just return 200, headers are set by Vercel
    """
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

        # Call Gemini API with site context
        response_text = call_gemini(user_message, history, site_context)

        return jsonify(response=response_text)

    except Exception as e:
        print(f"Chat endpoint error: {str(e)}")
        return jsonify(
            error="An error occurred processing your request",
            response="I'm having trouble right now. Please contact richwell.perez@gmail.com directly."
        ), 500
