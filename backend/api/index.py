from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# While testing, allow both your Pages URL and your custom domain
CORS(app, origins=[
    "https://richwellp.github.io"
])

@app.get("/")
def root():
    return jsonify(message="Hello from Flask on Vercel (hello.py)!")