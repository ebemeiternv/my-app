from flask import Flask, request, jsonify, send_from_directory, make_response, send_file
from flask_cors import CORS
import os
import requests
import logging
from io import BytesIO

# Initialize the Flask app and set up the static folder for React build
app = Flask(__name__, static_folder='static', static_url_path='/')

# Apply CORS to allow localhost:3000 and Heroku domain
CORS(app, resources={r"/*": {"origins": ["https://salty-beach-40498-7894fddcd70e.herokuapp.com", "http://localhost:3000"]}})

# Set up logging to log errors for better debugging
logging.basicConfig(level=logging.INFO)

# Serve React App (from build folder)
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
        # Handle preflight CORS request
        response = make_response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response, 200

    logging.info(f"Received request from {request.remote_addr}")  # Log the request IP address

    try:
        # Parse JSON data from the request
        data = request.get_json()
        if not data or 'ingredients' not in data:
            logging.error("No ingredients provided")
            return jsonify({"error": "No ingredients provided"}), 400

        # Extract ingredients and build the Spoonacular API request
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

        logging.info("Recipes successfully fetched")
        return jsonify(response.json())

    except Exception as e:
        logging.error(f"Error processing recipe request: {e}")
        return jsonify({"error": "Internal server error"}), 500


# Proxy route to fetch images from Spoonacular (to handle CORS and CORB issues)
@app.route('/api/proxy_image', methods=['GET'])
def proxy_image():
    image_url = request.args.get('url')
    if not image_url:
        logging.error("No image URL provided")
        return jsonify({"error": "No image URL provided"}), 400

    try:
        logging.info(f"Fetching image from: {image_url}")
        headers = {"User-Agent": "Mozilla/5.0"}  # Mimic a browser request
        response = requests.get(image_url, headers=headers)
        if response.status_code != 200:
            logging.error(f"Failed to fetch image: {response.status_code}")
            return jsonify({"error": f"Failed to fetch image: {response.status_code}"}), response.status_code

        img = BytesIO(response.content)
        file_response = make_response(send_file(img, mimetype=response.headers['Content-Type']))
        file_response.headers['Access-Control-Allow-Origin'] = '*'
        return file_response

    except Exception as e:
        logging.error(f"Error fetching image: {e}")
        return jsonify({"error": "Internal server error"}), 500


# New route to fetch recipe details using Spoonacular API
@app.route('/api/recipe_details/<int:recipe_id>', methods=['GET'])
def get_recipe_details(recipe_id):
    api_key = os.environ.get('SPOONACULAR_API_KEY')  # Use environment variable for the API key

    if not api_key:
        logging.error("API key not set")
        return jsonify({"error": "API key not set"}), 500

    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={api_key}'
    logging.info(f"Fetching recipe details for recipe ID: {recipe_id}")
    try:
        response = requests.get(url)
        if response.status_code != 200:
            logging.error(f"Failed to fetch recipe details: {response.status_code}, {response.text}")
            return jsonify({"error": "Failed to fetch recipe details"}), response.status_code

        logging.info("Recipe details successfully fetched")
        return jsonify(response.json())
    except Exception as e:
        logging.error(f"Error fetching recipe details: {e}")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    app.run(debug=True)
