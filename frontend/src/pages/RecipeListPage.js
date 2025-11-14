import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { ChefHat, Clock, Users, TrendingUp, Sparkles, Home, Filter, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import axios from "axios";
import RecipeCard from "../components/RecipeCard";
import FilterPanel from "../components/FilterPanel";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const RecipeListPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const ingredients = location.state?.ingredients || [];
  
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [filters, setFilters] = useState({
    difficulty: "",
    maxCookingTime: "",
    dietaryTags: []
  });
  const [showFilters, setShowFilters] = useState(false);

  useEffect(() => {
    if (ingredients.length > 0) {
      findMatchingRecipes();
    } else {
      navigate('/');
    }
  }, []);

  const findMatchingRecipes = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API}/recipes/find`, {
        ingredients,
        difficulty: filters.difficulty || undefined,
        max_cooking_time: filters.maxCookingTime ? parseInt(filters.maxCookingTime) : undefined,
        dietary_tags: filters.dietaryTags.length > 0 ? filters.dietaryTags : undefined
      });

      if (response.data.success) {
        setRecipes(response.data.recipes);
        if (response.data.recipes.length === 0) {
          toast.info("No matching recipes found. Try generating a new one!");
        }
      }
    } catch (error) {
      console.error("Error finding recipes:", error);
      toast.error("Failed to find recipes");
    } finally {
      setLoading(false);
    }
  };

  const generateNewRecipe = async () => {
    setGenerating(true);
    try {
      const response = await axios.post(`${API}/recipes/generate`, {
        ingredients,
        dietary_preferences: filters.dietaryTags,
        difficulty: filters.difficulty || undefined
      });

      if (response.data.success) {
        toast.success("New recipe generated!");
        // Add to beginning of list
        setRecipes([response.data.recipe, ...recipes]);
      }
    } catch (error) {
      console.error("Error generating recipe:", error);
      toast.error("Failed to generate recipe");
    } finally {
      setGenerating(false);
    }
  };

  const applyFilters = () => {
    findMatchingRecipes();
    setShowFilters(false);
  };

  return (
    <div className="min-h-screen">
      {/* Navigation */}
      <nav className="glass sticky top-0 z-50 border-b border-white/30">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <ChefHat className="w-8 h-8 text-orange-500" />
              <h1 className="text-2xl font-bold text-gradient">Recipe Results</h1>
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
                onClick={() => navigate('/saved')}
                data-testid="nav-saved-btn"
                className="hover:bg-orange-100"
              >
                My Recipes
              </Button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* Ingredients Summary */}
        <div className="card mb-8">
          <h3 className="text-xl font-bold mb-3">Your Ingredients:</h3>
          <div className="flex flex-wrap gap-2">
            {ingredients.map((ingredient, index) => (
              <span 
                key={index} 
                className="px-3 py-1 bg-orange-100 text-orange-800 rounded-full text-sm font-medium"
                data-testid={`ingredient-tag-${index}`}
              >
                {ingredient}
              </span>
            ))}
          </div>
        </div>

        {/* Actions Bar */}
        <div className="flex flex-wrap gap-4 mb-8 items-center justify-between">
          <div className="flex gap-3">
            <button
              onClick={generateNewRecipe}
              disabled={generating}
              className="btn btn-primary flex items-center"
              data-testid="generate-recipe-btn"
            >
              {generating ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Generating...
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4 mr-2" />
                  Generate New Recipe
                </>
              )}
            </button>
            
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="btn btn-secondary flex items-center"
              data-testid="toggle-filters-btn"
            >
              <Filter className="w-4 h-4 mr-2" />
              Filters
            </button>
          </div>
          
          <div className="text-gray-600 font-medium">
            {recipes.length} recipes found
          </div>
        </div>

        {/* Filter Panel */}
        {showFilters && (
          <div className="mb-8">
            <FilterPanel 
              filters={filters}
              setFilters={setFilters}
              onApply={applyFilters}
            />
          </div>
        )}

        {/* Recipes Grid */}
        {loading ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <div key={i} className="card">
                <div className="skeleton h-48 mb-4"></div>
                <div className="skeleton h-6 mb-2"></div>
                <div className="skeleton h-4 mb-4"></div>
                <div className="skeleton h-10"></div>
              </div>
            ))}
          </div>
        ) : recipes.length === 0 ? (
          <div className="card text-center py-16">
            <ChefHat className="w-16 h-16 mx-auto mb-4 text-gray-400" />
            <h3 className="text-2xl font-bold mb-2 text-gray-700">No recipes found</h3>
            <p className="text-gray-600 mb-6">Try generating a new AI-powered recipe!</p>
            <button 
              onClick={generateNewRecipe}
              disabled={generating}
              className="btn btn-primary"
            >
              {generating ? "Generating..." : "Generate Recipe"}
            </button>
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6" data-testid="recipes-grid">
            {recipes.map((recipe, index) => (
              <RecipeCard key={recipe.id || index} recipe={recipe} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default RecipeListPage;