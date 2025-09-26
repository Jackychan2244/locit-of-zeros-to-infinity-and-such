# main.py

import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

app = Flask(__name__)
CORS(app)

ORIGINAL_API_URL = "https://apieyhfveujcbdhss-21945c360009.herokuapp.com/api/chat/openai"

@app.route('/proxy', methods=['POST'])
def proxy_request():
    try:
        data = request.get_json()
        token = request.headers.get('x-my-app-token')

        if not data or not token:
            return jsonify({"error": "Missing data or token"}), 400

        headers = {
            'x-my-app-token': token,
            'Content-Type': 'application/json'
        }

        response = requests.post(ORIGINAL_API_URL, json=data, headers=headers, verify=False, timeout=30)
        response.raise_for_status()
        return jsonify(response.json())

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to proxy request", "details": str(e)}), 502
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

@app.route('/')
def index():
    return "Proxy is running!"

app.run(host='0.0.0.0', port=81)
