from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder='static/build')

# Apply CORS to allow all origins
CORS(app, resources={r"/*": {"origins": "*"}}, methods=["POST", "GET", "OPTIONS"])

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# Endpoint to get recipes from Spoonacular API
@app.route('/api/recipes', methods=['POST', 'OPTIONS'])
def get_recipes():
    if request.method == 'OPTIONS':
        # This handles the preflight OPTIONS request for CORS
        return jsonify({"message": "CORS preflight successful"}), 200

    data = request.get_json()  # Get the ingredients list from the frontend
    ingredients = ",".join(data['ingredients'])  # Join ingredients by comma

    api_key = 'your_spoonacular_api_key'  # Replace with your actual Spoonacular API key

    # Construct the Spoonacular API URL
    url = f'https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&apiKey={api_key}'

    # Send a GET request to the Spoonacular API
    response = requests.get(url)

    # Return the response back to the frontend
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
