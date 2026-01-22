from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', 'https://richwellp.github.io')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return

    def do_POST(self):
        """Handle chat requests"""
        try:
            # Set CORS headers
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', 'https://richwellp.github.io')
            self.end_headers()

            # Get request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            if not data or 'message' not in data:
                response = {'error': 'Message is required'}
                self.wfile.write(json.dumps(response).encode())
                return

            user_message = data.get('message', '').strip()
            if not user_message:
                response = {'error': 'Message cannot be empty'}
                self.wfile.write(json.dumps(response).encode())
                return

            # Import and call Gemini
            from gemini import call_gemini

            history = data.get('history', [])
            site_context = data.get('site_context', {})

            response_text = call_gemini(user_message, history, site_context)

            response = {'response': response_text}
            self.wfile.write(json.dumps(response).encode())

        except Exception as e:
            print(f"Chat error: {str(e)}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', 'https://richwellp.github.io')
            self.end_headers()
            response = {
                'error': 'An error occurred',
                'response': "I'm having trouble right now. Please contact richwell.perez@gmail.com directly."
            }
            self.wfile.write(json.dumps(response).encode())
