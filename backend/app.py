from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests

# Define the Flask app and set the correct static folder
app = Flask(__name__, static_folder=os.path.join('static', 'build'))

# Apply CORS to allow all origins
CORS(app, resources={r"/*": {"origins": "*"}}, methods=["POST", "GET", "OPTIONS"])

# Serve the React App (static files)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
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
    api_key = '6ff9812470314998a8db9f0087cbf3c2'

    # Query Spoonacular API with ingredients
    url = f'https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&apiKey={api_key}'
    response = requests.get(url)

    return jsonify(response.json())

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
