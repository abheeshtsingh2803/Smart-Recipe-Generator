import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Upload, Sparkles, ChefHat, Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const HomePage = () => {
  const navigate = useNavigate();
  const [ingredientInput, setIngredientInput] = useState("");
  const [recognizedIngredients, setRecognizedIngredients] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [selectedImage, setSelectedImage] = useState(null);

  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Check file type
    if (!['image/jpeg', 'image/png', 'image/webp'].includes(file.type)) {
      toast.error("Please upload a JPEG, PNG, or WEBP image");
      return;
    }

    setIsUploading(true);
    setSelectedImage(URL.createObjectURL(file));

    try {
      // Convert to base64
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = async () => {
        const base64String = reader.result.split(',')[1];
        
        const response = await axios.post(`${API}/ingredients/recognize`, {
          image_base64: base64String
        });

        if (response.data.success) {
          setRecognizedIngredients(response.data.ingredients);
          toast.success(`Recognized ${response.data.ingredients.length} ingredients!`);
        }
      };
    } catch (error) {
      console.error("Error recognizing ingredients:", error);
      toast.error("Failed to recognize ingredients. Please try again.");
    } finally {
      setIsUploading(false);
    }
  };

  const handleTextInput = () => {
    if (!ingredientInput.trim()) {
      toast.error("Please enter some ingredients");
      return;
    }

    const ingredients = ingredientInput
      .split(',')
      .map(i => i.trim())
      .filter(i => i.length > 0);

    setRecognizedIngredients(ingredients);
    toast.success(`Added ${ingredients.length} ingredients`);
  };

  const handleFindRecipes = () => {
    if (recognizedIngredients.length === 0) {
      toast.error("Please add some ingredients first");
      return;
    }

    navigate('/recipes', { state: { ingredients: recognizedIngredients } });
  };

  const removeIngredient = (index) => {
    setRecognizedIngredients(prev => prev.filter((_, i) => i !== index));
  };

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Decorative Background Elements */}
      <div className="absolute top-20 right-10 w-32 h-32 bg-gradient-to-br from-orange-300 to-orange-400 rounded-full opacity-20 blur-3xl animate-float"></div>
      <div className="absolute bottom-20 left-10 w-40 h-40 bg-gradient-to-br from-yellow-300 to-orange-300 rounded-full opacity-20 blur-3xl" style={{animation: 'float 4s ease-in-out infinite'}}></div>
      
      {/* Navigation */}
      <nav className="glass sticky top-0 z-50 border-b border-white/30">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <ChefHat className="w-8 h-8 text-orange-500" />
              <h1 className="text-2xl font-bold text-gradient">Smart Recipe</h1>
            </div>
            <div className="flex space-x-4">
              <Button 
                variant="ghost" 
                onClick={() => navigate('/saved')}
                data-testid="nav-saved-recipes-btn"
                className="hover:bg-orange-100"
              >
                My Recipes
              </Button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="max-w-6xl mx-auto px-6 py-16">
        <div className="text-center mb-16 animate-fade-in">
          <h2 className="text-5xl sm:text-6xl font-bold mb-6 text-gradient leading-tight">
            Discover Delicious Recipes
          </h2>
          <p className="text-lg text-gray-700 max-w-2xl mx-auto">
            Upload a photo of your ingredients or type them in, and let AI create amazing recipes just for you
          </p>
        </div>

        {/* Input Section */}
        <div className="grid md:grid-cols-2 gap-8 mb-12">
          {/* Image Upload */}
          <div className="card animate-fade-in" style={{animationDelay: '0.2s'}}>
            <div className="text-center">
              <Upload className="w-12 h-12 mx-auto mb-4 text-orange-500" />
              <h3 className="text-2xl font-bold mb-3">Upload Image</h3>
              <p className="text-gray-600 mb-6">Take a photo of your ingredients</p>
              
              <label 
                htmlFor="image-upload" 
                className="btn btn-primary cursor-pointer inline-block"
                data-testid="upload-image-btn"
              >
                {isUploading ? "Analyzing..." : "Choose Image"}
              </label>
              <input
                id="image-upload"
                type="file"
                accept="image/jpeg,image/png,image/webp"
                onChange={handleImageUpload}
                className="hidden"
                data-testid="image-upload-input"
              />

              {selectedImage && (
                <div className="mt-6">
                  <img 
                    src={selectedImage} 
                    alt="Uploaded ingredients" 
                    className="w-full h-48 object-cover rounded-xl"
                    data-testid="uploaded-image-preview"
                  />
                </div>
              )}
            </div>
          </div>

          {/* Text Input */}
          <div className="card animate-fade-in" style={{animationDelay: '0.3s'}}>
            <div className="text-center">
              <Search className="w-12 h-12 mx-auto mb-4 text-orange-500" />
              <h3 className="text-2xl font-bold mb-3">Type Ingredients</h3>
              <p className="text-gray-600 mb-6">List your ingredients separated by commas</p>
              
              <textarea
                value={ingredientInput}
                onChange={(e) => setIngredientInput(e.target.value)}
                placeholder="e.g., chicken, tomatoes, garlic, onions"
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-orange-400 focus:outline-none mb-4 h-32 resize-none"
                data-testid="ingredient-text-input"
              />
              
              <button 
                onClick={handleTextInput} 
                className="btn btn-primary w-full"
                data-testid="add-ingredients-btn"
              >
                Add Ingredients
              </button>
            </div>
          </div>
        </div>

        {/* Recognized Ingredients */}
        {recognizedIngredients.length > 0 && (
          <div className="card mb-12 animate-fade-in" data-testid="recognized-ingredients-section">
            <h3 className="text-2xl font-bold mb-6 flex items-center">
              <Sparkles className="w-6 h-6 mr-2 text-orange-500" />
              Your Ingredients ({recognizedIngredients.length})
            </h3>
            <div className="flex flex-wrap gap-3 mb-6">
              {recognizedIngredients.map((ingredient, index) => (
                <div 
                  key={index} 
                  className="px-4 py-2 bg-gradient-to-r from-orange-100 to-orange-200 rounded-full flex items-center space-x-2 hover:shadow-md transition-all"
                  data-testid={`ingredient-chip-${index}`}
                >
                  <span className="font-medium text-orange-900">{ingredient}</span>
                  <button 
                    onClick={() => removeIngredient(index)}
                    className="text-orange-700 hover:text-orange-900 font-bold"
                    data-testid={`remove-ingredient-${index}`}
                  >
                    ×
                  </button>
                </div>
              ))}
            </div>
            
            <button 
              onClick={handleFindRecipes}
              className="btn btn-primary w-full text-lg py-4 shadow-glow"
              data-testid="find-recipes-btn"
            >
              <Sparkles className="w-5 h-5 mr-2 inline" />
              Find Recipes
            </button>
          </div>
        )}

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-6 mt-16">
          <div className="card text-center animate-fade-in" style={{animationDelay: '0.4s'}}>
            <div className="w-16 h-16 bg-gradient-to-br from-orange-400 to-orange-500 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <ChefHat className="w-8 h-8 text-white" />
            </div>
            <h4 className="text-xl font-bold mb-2">AI-Powered</h4>
            <p className="text-gray-600">Smart recipe generation using GPT-4</p>
          </div>
          
          <div className="card text-center animate-fade-in" style={{animationDelay: '0.5s'}}>
            <div className="w-16 h-16 bg-gradient-to-br from-green-400 to-green-500 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <Sparkles className="w-8 h-8 text-white" />
            </div>
            <h4 className="text-xl font-bold mb-2">Personalized</h4>
            <p className="text-gray-600">Filter by dietary preferences and allergies</p>
          </div>
          
          <div className="card text-center animate-fade-in" style={{animationDelay: '0.6s'}}>
            <div className="w-16 h-16 bg-gradient-to-br from-purple-400 to-purple-500 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <Upload className="w-8 h-8 text-white" />
            </div>
            <h4 className="text-xl font-bold mb-2">Easy to Use</h4>
            <p className="text-gray-600">Upload images or type ingredients</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;