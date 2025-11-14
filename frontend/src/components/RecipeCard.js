import React from "react";
import { useNavigate } from "react-router-dom";
import { Clock, Users, TrendingUp, Star } from "lucide-react";

const RecipeCard = ({ recipe, showRating = false }) => {
  const navigate = useNavigate();

  const getDifficultyColor = (difficulty) => {
    switch(difficulty?.toLowerCase()) {
      case 'easy': return 'bg-green-100 text-green-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'hard': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div 
      className="card cursor-pointer group"
      onClick={() => navigate(`/recipe/${recipe.id}`)}
      data-testid={`recipe-card-${recipe.id}`}
    >
      {/* Recipe Image Placeholder */}
      <div className="w-full h-48 bg-gradient-to-br from-orange-200 to-orange-300 rounded-xl mb-4 flex items-center justify-center overflow-hidden relative">
        <div className="text-6xl group-hover:scale-110 transition-transform duration-300">🍳</div>
        {recipe.match_score && (
          <div className="absolute top-3 right-3 bg-white/95 px-3 py-1 rounded-full flex items-center space-x-1 shadow-md">
            <TrendingUp className="w-4 h-4 text-orange-600" />
            <span className="font-bold text-orange-600 text-sm">{recipe.match_score}%</span>
          </div>
        )}
      </div>

      {/* Recipe Info */}
      <div className="flex flex-wrap gap-2 mb-3">
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(recipe.difficulty)}`}>
          {recipe.difficulty}
        </span>
        <span className="px-2 py-1 bg-purple-100 text-purple-800 rounded-full text-xs font-medium">
          {recipe.cuisine}
        </span>
      </div>

      <h3 className="text-xl font-bold mb-3 group-hover:text-orange-600 transition-colors" data-testid="recipe-card-name">
        {recipe.name}
      </h3>

      <div className="flex items-center justify-between text-sm text-gray-600 mb-4">
        <div className="flex items-center">
          <Clock className="w-4 h-4 mr-1" />
          <span>{recipe.cooking_time} min</span>
        </div>
        <div className="flex items-center">
          <Users className="w-4 h-4 mr-1" />
          <span>{recipe.serving_size} servings</span>
        </div>
      </div>

      {showRating && recipe.user_rating && (
        <div className="flex items-center mb-3 pb-3 border-t pt-3">
          <span className="text-sm font-medium mr-2">Your Rating:</span>
          <div className="flex">
            {[...Array(5)].map((_, i) => (
              <Star 
                key={i}
                className={`w-4 h-4 ${i < recipe.user_rating ? 'fill-orange-500 text-orange-500' : 'text-gray-300'}`}
              />
            ))}
          </div>
        </div>
      )}

      <button 
        className="btn btn-primary w-full text-sm py-2"
        onClick={(e) => {
          e.stopPropagation();
          navigate(`/recipe/${recipe.id}`);
        }}
        data-testid={`view-recipe-btn-${recipe.id}`}
      >
        View Recipe
      </button>
    </div>
  );
};

export default RecipeCard;