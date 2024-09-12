import React, { useState } from 'react';

function RecipeForm() {
  const [ingredients, setIngredients] = useState('');
  const [recipes, setRecipes] = useState([]);  // State to store recipe data
  const [error, setError] = useState(null);    // State to handle any error

  // Update this URL to point to your deployed Heroku app
  const API_URL = 'https://salty-beach-40498-7894fddcd70e.herokuapp.com/api/recipes';

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
    } catch (err) {
      console.error('Error:', err);
      setError('Failed to fetch recipes. Please try again.');  // Set error message
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
        />
        <button type="submit">Get Recipes</button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      <div>
        {recipes.length > 0 ? (
          <ul>
            {recipes.map((recipe) => (
              <li key={recipe.id}>
                <h3>{recipe.title}</h3>
                <img src={recipe.image} alt={recipe.title} />
                <p>Likes: {recipe.likes}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p>No recipes yet. Submit ingredients to get results!</p>
        )}
      </div>
    </div>
  );
}

export default RecipeForm;
