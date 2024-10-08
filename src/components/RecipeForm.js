import React, { useState } from 'react';

function RecipeForm() {
  const [ingredients, setIngredients] = useState('');
  const [recipes, setRecipes] = useState([]);  // State to store recipe data
  const [selectedRecipe, setSelectedRecipe] = useState(null); // State to store selected recipe details
  const [error, setError] = useState(null);    // State to handle any error

  const API_URL = 'https://salty-beach-40498-7894fddcd70e.herokuapp.com/api/recipes';
  const SPOONACULAR_RECIPE_DETAILS_URL = 'https://api.spoonacular.com/recipes/';
  const SPOONACULAR_API_KEY = '6ff9812470314998a8db9f0087cbf3c2'; // Your API key

  // Function to handle fetching recipe by ingredients
  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ingredients: ingredients.split(',') }), // Send ingredients as array
      });

      if (!response.ok) {
        throw new Error('Error fetching recipes');
      }

      const data = await response.json();
      setRecipes(data);   // Update recipes state with received data
      setError(null);     // Clear error state if the request is successful
      setSelectedRecipe(null); // Reset selected recipe when fetching new recipes
      console.log('Recipes fetched:', data); // Debugging log
    } catch (err) {
      console.error('Error:', err);
      setError('Failed to fetch recipes. Please try again.');
    }
  };

  // Function to handle fetching recipe details
  const fetchRecipeDetails = async (id) => {
    console.log(`Fetching details for recipe ID: ${id}`); // Debugging log

    try {
      const response = await fetch(`${SPOONACULAR_RECIPE_DETAILS_URL}${id}/information?apiKey=${SPOONACULAR_API_KEY}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        mode: 'cors'  // Adding CORS support explicitly
      });

      if (!response.ok) {
        throw new Error(`Error fetching recipe details for ID ${id}`);
      }

      const recipeDetails = await response.json();
      console.log('Recipe details fetched:', recipeDetails); // Log fetched details

      setSelectedRecipe(recipeDetails);  // Update selected recipe state
      console.log('Selected recipe state updated:', recipeDetails); // Debugging log
    } catch (err) {
      console.error('Error fetching recipe details:', err);
      setError(`Failed to fetch recipe details for ID ${id}`);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter ingredients separated by commas"
          value={ingredients}
          onChange={(e) => setIngredients(e.target.value)}
          id="ingredient-input"  // Added an ID attribute to avoid the autofill warning
        />
        <button type="submit">Get Recipes</button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      <div>
        {recipes.length > 0 ? (
          <ul>
            {recipes.map((recipe) => (
              <li key={recipe.id} onClick={() => {
                console.log(`Recipe clicked: ${recipe.id}`);
                fetchRecipeDetails(recipe.id);
              }}>
                <h3>{recipe.title}</h3>
                <img
                  src={recipe.image}
                  alt={recipe.title}
                  crossOrigin="anonymous"  // Adding crossOrigin to prevent CORB issues
                />
                <p>Likes: {recipe.likes}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p>No recipes yet. Submit ingredients to get results!</p>
        )}

        {/* Render selected recipe details */}
        {selectedRecipe && (
          <div>
            <h2>{selectedRecipe.title}</h2>
            <img src={selectedRecipe.image} alt={selectedRecipe.title} />
            <p><strong>Ingredients:</strong></p>
            <ul>
              {selectedRecipe.extendedIngredients?.map((ingredient) => (
                <li key={ingredient.id}>{ingredient.original}</li>
              ))}
            </ul>
            <p><strong>Instructions:</strong> {selectedRecipe.instructions}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default RecipeForm;
