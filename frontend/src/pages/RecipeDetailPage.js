import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { ChefHat, Clock, Users, Heart, Home, Star, BookmarkPlus, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import axios from "axios";
import NutritionInfo from "../components/NutritionInfo";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const RecipeDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [recipe, setRecipe] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [rating, setRating] = useState(0);
  const [servingSize, setServingSize] = useState(4);

  useEffect(() => {
    fetchRecipe();
  }, [id]);

  const fetchRecipe = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/recipes/${id}`);
      if (response.data.success) {
        setRecipe(response.data.recipe);
        setServingSize(response.data.recipe.serving_size);
      }
    } catch (error) {
      console.error("Error fetching recipe:", error);
      toast.error("Failed to load recipe");
      navigate('/recipes');
    } finally {
      setLoading(false);
    }
  };

  const saveRecipe = async () => {
    if (rating === 0) {
      toast.error("Please rate the recipe before saving");
      return;
    }

    setSaving(true);
    try {
      const userSession = localStorage.getItem('user_session') || 
        `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      localStorage.setItem('user_session', userSession);

      const response = await axios.post(`${API}/user/saved-recipes`, {
        user_session: userSession,
        recipe_id: id,
        rating: rating,
        notes: ""
      });

      if (response.data.success) {
        toast.success("Recipe saved to your collection!");
      }
    } catch (error) {
      console.error("Error saving recipe:", error);
      toast.error("Failed to save recipe");
    } finally {
      setSaving(false);
    }
  };

  const getDifficultyColor = (difficulty) => {
    switch(difficulty?.toLowerCase()) {
      case 'easy': return 'bg-green-100 text-green-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'hard': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="w-12 h-12 animate-spin text-orange-500" />
      </div>
    );
  }

  if (!recipe) {
    return null;
  }

  return (
    <div className="min-h-screen">
      {/* Navigation */}
      <nav className="glass sticky top-0 z-50 border-b border-white/30">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <ChefHat className="w-8 h-8 text-orange-500" />
              <h1 className="text-2xl font-bold text-gradient">Recipe Details</h1>
            </div>
            <div className="flex space-x-3">
              <Button 
                variant="ghost" 
                onClick={() => navigate('/')}
                data-testid="nav-home-btn"
                className="hover:bg-orange-100"
              >
                <Home className="w-4 h-4 mr-2" />
                Home
              </Button>
              <Button 
                variant="ghost" 
                onClick={() => navigate(-1)}
                data-testid="nav-back-btn"
                className="hover:bg-orange-100"
              >
                Back
              </Button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-5xl mx-auto px-6 py-12">
        {/* Recipe Header */}
        <div className="card mb-8" data-testid="recipe-detail-header">
          <div className="flex flex-wrap gap-2 mb-4">
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${getDifficultyColor(recipe.difficulty)}`}>
              {recipe.difficulty}
            </span>
            <span className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm font-medium">
              {recipe.cuisine}
            </span>
            {recipe.dietary_tags?.map((tag, index) => (
              <span key={index} className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                {tag}
              </span>
            ))}
            {recipe.match_score && (
              <span className="px-3 py-1 bg-orange-100 text-orange-800 rounded-full text-sm font-medium">
                {recipe.match_score}% match
              </span>
            )}
          </div>

          <h2 className="text-4xl font-bold mb-6 text-gradient" data-testid="recipe-name">{recipe.name}</h2>

          <div className="flex flex-wrap gap-6 text-gray-700">
            <div className="flex items-center">
              <Clock className="w-5 h-5 mr-2 text-orange-500" />
              <span className="font-medium">{recipe.cooking_time} mins</span>
            </div>
            <div className="flex items-center">
              <Users className="w-5 h-5 mr-2 text-orange-500" />
              <span className="font-medium">{servingSize} servings</span>
            </div>
          </div>

          {/* Rating */}
          <div className="mt-6 border-t pt-6">
            <p className="text-sm font-medium mb-2">Rate this recipe:</p>
            <div className="flex items-center space-x-2">
              {[1, 2, 3, 4, 5].map((star) => (
                <button
                  key={star}
                  onClick={() => setRating(star)}
                  data-testid={`star-${star}`}
                  className="transition-all hover:scale-110"
                >
                  <Star 
                    className={`w-8 h-8 ${star <= rating ? 'fill-orange-500 text-orange-500' : 'text-gray-300'}`}
                  />
                </button>
              ))}
            </div>
          </div>

          {/* Save Button */}
          <button
            onClick={saveRecipe}
            disabled={saving || rating === 0}
            className="btn btn-primary mt-6 w-full sm:w-auto"
            data-testid="save-recipe-btn"
          >
            {saving ? (
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
            ) : (
              <BookmarkPlus className="w-4 h-4 mr-2" />
            )}
            {saving ? "Saving..." : "Save to My Recipes"}
          </button>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Ingredients */}
          <div className="lg:col-span-2">
            <div className="card mb-8">
              <h3 className="text-2xl font-bold mb-6">Ingredients</h3>
              <ul className="space-y-3" data-testid="ingredients-list">
                {recipe.ingredients?.map((ingredient, index) => (
                  <li key={index} className="flex items-start">
                    <span className="w-2 h-2 bg-orange-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                    <span className="text-gray-700">{ingredient}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Instructions */}
            <div className="card">
              <h3 className="text-2xl font-bold mb-6">Instructions</h3>
              <ol className="space-y-4" data-testid="instructions-list">
                {recipe.instructions?.map((instruction, index) => (
                  <li key={index} className="flex items-start">
                    <span className="w-8 h-8 bg-gradient-to-br from-orange-400 to-orange-500 text-white rounded-full flex items-center justify-center font-bold mr-4 flex-shrink-0">
                      {index + 1}
                    </span>
                    <p className="text-gray-700 pt-1">{instruction}</p>
                  </li>
                ))}
              </ol>
            </div>
          </div>

          {/* Nutrition Info */}
          <div className="lg:col-span-1">
            <NutritionInfo nutrition={recipe.nutrition} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default RecipeDetailPage;