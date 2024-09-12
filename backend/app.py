from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests
import logging

# Initialize the Flask app and set up static folder
app = Flask(__name__, static_folder='static/build', static_url_path='/')

# Apply CORS to allow all origins and all methods (GET, POST, OPTIONS)
CORS(app, resources={r"/*": {"origins": "*"}}, methods=["POST", "GET", "OPTIONS"])

# Set up logging to log errors for better debugging
logging.basicConfig(level=logging.INFO)

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        logging.info(f"Serving static file: {path}")
        return send_from_directory(app.static_folder, path)
    else:
        logging.info("Serving index.html")
        return send_from_directory(app.static_folder, 'index.html')

# Recipe API route
@app.route('/api/recipes', methods=['POST', 'OPTIONS'])
def get_recipes():
    if request.method == 'OPTIONS':
        logging.info("CORS preflight request handled")
        return jsonify({"message": "CORS preflight successful"}), 200

    try:
        data = request.get_json()
        ingredients = ",".join(data['ingredients'])
        api_key = os.environ.get('SPOONACULAR_API_KEY')  # Use environment variable for the API key

        if not api_key:
            logging.error("API key not set")
            return jsonify({"error": "API key not set"}), 500

        url = f'https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&apiKey={api_key}'
        logging.info(f"Fetching recipes for ingredients: {ingredients}")
        response = requests.get(url)

        if response.status_code != 200:
            logging.error(f"Failed to fetch recipes: {response.status_code}, {response.text}")
            return jsonify({"error": "Failed to fetch recipes"}), response.status_code

        return jsonify(response.json())

    except Exception as e:
        logging.error(f"Error processing recipe request: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
