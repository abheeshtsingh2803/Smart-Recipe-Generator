from typing import List, Dict, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from services.openai_service import OpenAIService
from services.recipe_service import RecipeMatchingService
from models.recipe import Recipe
import logging

logger = logging.getLogger(__name__)

class RecipeController:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.openai_service = OpenAIService()
        self.matching_service = RecipeMatchingService()
    
    async def generate_recipe_from_ingredients(
        self, 
        ingredients: List[str],
        dietary_preferences: List[str] = [],
        cuisine_preference: Optional[str] = None,
        difficulty: Optional[str] = None
    ) -> Dict:
        """Generate a new recipe using AI"""
        try:
            recipe_data = await self.openai_service.generate_recipe(
                ingredients=ingredients,
                dietary_preferences=dietary_preferences,
                cuisine_preference=cuisine_preference,
                difficulty=difficulty
            )
            
            # Save to database
            recipe_obj = Recipe(**recipe_data)
            doc = recipe_obj.model_dump()
            doc['created_at'] = doc['created_at'].isoformat()
            
            await self.db.recipes.insert_one(doc)
            
            return recipe_data
        except Exception as e:
            logger.error(f"Error generating recipe: {str(e)}")
            raise
    
    async def find_matching_recipes(
        self,
        ingredients: List[str],
        difficulty: Optional[str] = None,
        max_cooking_time: Optional[int] = None,
        dietary_tags: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[Dict]:
        """Find recipes from database that match available ingredients"""
        try:
            # Get all recipes from database
            recipes = await self.db.recipes.find({}, {"_id": 0}).to_list(1000)
            
            # Calculate match scores
            for recipe in recipes:
                recipe['match_score'] = self.matching_service.calculate_match_score(
                    recipe.get('ingredients', []),
                    ingredients
                )
            
            # Filter recipes
            filtered = self.matching_service.filter_recipes_by_criteria(
                recipes=recipes,
                difficulty=difficulty,
                max_cooking_time=max_cooking_time,
                dietary_tags=dietary_tags,
                min_match_score=30  # At least 30% match
            )
            
            # Sort by match score
            filtered.sort(key=lambda x: x.get('match_score', 0), reverse=True)
            
            return filtered[:limit]
        except Exception as e:
            logger.error(f"Error finding matching recipes: {str(e)}")
            raise
    
    async def get_recipe_by_id(self, recipe_id: str) -> Optional[Dict]:
        """Get a specific recipe by ID"""
        try:
            recipe = await self.db.recipes.find_one({"id": recipe_id}, {"_id": 0})
            return recipe
        except Exception as e:
            logger.error(f"Error getting recipe: {str(e)}")
            raise
    
    async def adjust_serving_size(self, recipe_id: str, new_serving_size: int) -> Dict:
        """Adjust recipe quantities for different serving sizes"""
        try:
            recipe = await self.get_recipe_by_id(recipe_id)
            if not recipe:
                raise ValueError("Recipe not found")
            
            original_serving = recipe['serving_size']
            multiplier = new_serving_size / original_serving
            
            # Note: This is a simplified version. In production, you'd parse and adjust ingredient quantities
            recipe['serving_size'] = new_serving_size
            recipe['note'] = f"Recipe adjusted from {original_serving} to {new_serving_size} servings"
            
            return recipe
        except Exception as e:
            logger.error(f"Error adjusting serving size: {str(e)}")
            raise