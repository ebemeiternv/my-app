from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests

app = Flask(__name__, static_folder='static')

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

# Recipe API route
@app.route('/api/recipes', methods=['POST', 'OPTIONS'])
def get_recipes():
    if request.method == 'OPTIONS':
        return jsonify({"message": "CORS preflight successful"}), 200

    data = request.get_json()
    ingredients = ",".join(data['ingredients'])
    api_key = os.environ.get('SPOONACULAR_API_KEY')  # Use environment variable for the API key

    if not api_key:
        return jsonify({"error": "API key not set"}), 500

    url = f'https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&apiKey={api_key}'
    response = requests.get(url)

    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
