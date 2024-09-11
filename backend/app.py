from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)

# Apply CORS with explicit origins and methods
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, methods=["POST", "GET", "OPTIONS"])


# Home route
@app.route('/')
def home():
    return 'Welcome to the Recipe Recommendation App!'


# Endpoint to get recipes from Spoonacular API
@app.route('/api/recipes', methods=['POST'])
def get_recipes():
    data = request.get_json()  # Get the ingredients list from the frontend
    ingredients = ",".join(data['ingredients'])  # Join ingredients by comma

    api_key = '6ff9812470314998a8db9f0087cbf3c2'  # Your actual Spoonacular API key

    # Construct the Spoonacular API URL
    url = f'https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&apiKey={api_key}'

    # Send a GET request to the Spoonacular API
    response = requests.get(url)

    # Print the response for debugging
    print(response.json())  # Debugging: print the Spoonacular API response

    # Return the response back to the frontend
    return jsonify(response.json())


if __name__ == '__main__':
    app.run(debug=True)


