# See https://github.com/sartography/spiff-arena/blob/main/spiffworkflow-backend/bin/run_message_start_event_with_api#L39
import os
import logging
from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv
import requests
from gunicorn.app.wsgiapp import run

app = Flask(__name__)
load_dotenv()  # Load environment variables from .env file

# Configure logging
logging.basicConfig(level=logging.INFO)

# Swagger UI setup
SWAGGER_URL = '/api/docs'  # URL for accessing Swagger UI
API_URL = '/static/swagger.json'  # URL for the Swagger JSON file

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Connector Webhook"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

def verify_basic_auth(request):
    auth = request.authorization
    if not auth or not (auth.username and auth.password):
        return False

    expected_username = os.getenv("WEBHOOK_USERNAME", "default_username")
    expected_password = os.getenv("WEBHOOK_PASSWORD", "default_password")

    return auth.username == expected_username and auth.password == expected_password

def get_access_token():
    """Retrieve an access token using client credentials."""
    token_data = {
        "client_id": os.getenv("CLIENT_ID", "default_client_id"),
        "client_secret": os.getenv("CLIENT_SECRET", "default_client_secret"),
        "grant_type": "password",
        "username": os.getenv("USERNAME", "admin"),
        "password": os.getenv("PASSWORD", "admin")
    }
    token_url = os.getenv("TOKEN_URL", "http://localhost/token")
    response = requests.post(token_url, data=token_data)
    if response.status_code != 200:
        logging.error("Failed to acquire token: %s", response.text)
        response.raise_for_status()
    return response.json().get("access_token")

@app.errorhandler(Exception)
def handle_exception(e):
    """Global error handler."""
    logging.error("Unhandled exception: %s", str(e))
    return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@app.route('/', methods=['POST'])
def webhook():
    if not verify_basic_auth(request):
        return jsonify({"error": "Unauthorized"}), 401

    try:
        access_token = get_access_token()
    except requests.RequestException as e:
        return jsonify({"error": "Failed to acquire token", "message": str(e)}), 500

    # Process the webhook payload
    payload = request.json
    message_name = payload.get("message-name")
    data = payload.get("data")

    if not message_name or not data:
        return jsonify({"error": "Invalid payload"}), 400

    # Forward the data to another API
    api_url = os.getenv("API_URL", "http://localhost/api/")
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    try:
        api_response = requests.post(api_url + message_name, json=data, headers=headers)
        if api_response.status_code == 200:
            return jsonify({"success": True}), 200
        else:
            logging.error("Failed to forward data: %s", api_response.text)
            return jsonify({"error": "Failed to forward data", "message": api_response.text}), 500
    except requests.RequestException as e:
        logging.error("Error while forwarding data: %s", str(e))
        return jsonify({"error": "Failed to forward data", "message": str(e)}), 500

if __name__ == "__main__":
    run()