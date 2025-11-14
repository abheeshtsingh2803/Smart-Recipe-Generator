import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { ChefHat, Home, Trash2, Heart, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import axios from "axios";
import RecipeCard from "../components/RecipeCard";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const SavedRecipesPage = () => {
  const navigate = useNavigate();
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSavedRecipes();
  }, []);

  const fetchSavedRecipes = async () => {
    setLoading(true);
    try {
      const userSession = localStorage.getItem('user_session');
      if (!userSession) {
        setLoading(false);
        return;
      }

      const response = await axios.get(`${API}/user/saved-recipes/${userSession}`);
      if (response.data.success) {
        setRecipes(response.data.recipes);
      }
    } catch (error) {
      console.error("Error fetching saved recipes:", error);
      toast.error("Failed to load saved recipes");
    } finally {
      setLoading(false);
    }
  };

  const deleteRecipe = async (recipeId) => {
    try {
      const userSession = localStorage.getItem('user_session');
      const response = await axios.delete(`${API}/user/saved-recipes/${userSession}/${recipeId}`);
      
      if (response.data.success) {
        setRecipes(recipes.filter(r => r.id !== recipeId));
        toast.success("Recipe removed from favorites");
      }
    } catch (error) {
      console.error("Error deleting recipe:", error);
      toast.error("Failed to remove recipe");
    }
  };

  return (
    <div className="min-h-screen">
      {/* Navigation */}
      <nav className="glass sticky top-0 z-50 border-b border-white/30">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Heart className="w-8 h-8 text-orange-500 fill-orange-500" />
              <h1 className="text-2xl font-bold text-gradient">My Recipes</h1>
            </div>
            <Button 
              variant="ghost" 
              onClick={() => navigate('/')}
              data-testid="nav-home-btn"
              className="hover:bg-orange-100"
            >
              <Home className="w-4 h-4 mr-2" />
              Home
            </Button>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-6 py-12">
        <div className="mb-8">
          <h2 className="text-3xl font-bold mb-2">Your Saved Recipes</h2>
          <p className="text-gray-600">All your favorite recipes in one place</p>
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-20">
            <Loader2 className="w-12 h-12 animate-spin text-orange-500" />
          </div>
        ) : recipes.length === 0 ? (
          <div className="card text-center py-16">
            <Heart className="w-16 h-16 mx-auto mb-4 text-gray-400" />
            <h3 className="text-2xl font-bold mb-2 text-gray-700">No saved recipes yet</h3>
            <p className="text-gray-600 mb-6">Start exploring and save your favorite recipes!</p>
            <button 
              onClick={() => navigate('/')}
              className="btn btn-primary"
              data-testid="start-exploring-btn"
            >
              Start Exploring
            </button>
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6" data-testid="saved-recipes-grid">
            {recipes.map((recipe) => (
              <div key={recipe.id} className="relative">
                <RecipeCard recipe={recipe} showRating={true} />
                <button
                  onClick={() => deleteRecipe(recipe.id)}
                  className="absolute top-4 right-4 p-2 bg-red-500 text-white rounded-full hover:bg-red-600 transition-all shadow-lg"
                  data-testid={`delete-recipe-${recipe.id}`}
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default SavedRecipesPage;