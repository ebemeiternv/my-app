import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [ingredients, setIngredients] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [searched, setSearched] = useState(false); // Track if a search has been made

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSearched(true); // Mark that a search has been made
    try {
      // Use the Heroku URL instead of localhost
      const response = await axios.post('https://salty-beach-40498.herokuapp.com/api/recipes', {
        ingredients: ingredients.split(',').map(item => item.trim())
      });
      setRecommendations(response.data);
    } catch (error) {
      console.error("There was an error fetching the data:", error);
    }
  };

  return (
    <div>
      <h1>Recipe Recommendation App</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={ingredients}
          onChange={(e) => setIngredients(e.target.value)}
          placeholder="Enter ingredients separated by commas"
        />
        <button type="submit">Get Recommendations</button>
      </form>
      <ul>
        {searched ? ( // Only display recommendations or 'No recommendations' after a search
          recommendations.length > 0 ? (
            recommendations.map((recipe, index) => (
              <li key={index}>
                <h2>{recipe.title}</h2>
                <img src={recipe.image} alt={recipe.title} width="100" />
                <p>Used ingredients: {recipe.usedIngredientCount}</p>
                <p>Missed ingredients: {recipe.missedIngredientCount}</p>
              </li>
            ))
          ) : (
            <p>No recommendations available</p>
          )
        ) : (
          <p>Enter ingredients to get recipe recommendations</p>
        )}
      </ul>
    </div>
  );
}

export default App;
