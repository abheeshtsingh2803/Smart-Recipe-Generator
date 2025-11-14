from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from controllers.recipe_controller import RecipeController

router = APIRouter(prefix="/recipes", tags=["recipes"])

# Request/Response Models
class GenerateRecipeRequest(BaseModel):
    ingredients: List[str]
    dietary_preferences: List[str] = []
    cuisine_preference: Optional[str] = None
    difficulty: Optional[str] = None

class FindRecipesRequest(BaseModel):
    ingredients: List[str]
    difficulty: Optional[str] = None
    max_cooking_time: Optional[int] = None
    dietary_tags: Optional[List[str]] = None

class AdjustServingRequest(BaseModel):
    recipe_id: str
    new_serving_size: int

def init_recipe_routes(db: AsyncIOMotorDatabase):
    controller = RecipeController(db)
    
    @router.post("/generate")
    async def generate_recipe(request: GenerateRecipeRequest):
        """Generate a new recipe using AI based on ingredients"""
        try:
            recipe = await controller.generate_recipe_from_ingredients(
                ingredients=request.ingredients,
                dietary_preferences=request.dietary_preferences,
                cuisine_preference=request.cuisine_preference,
                difficulty=request.difficulty
            )
            return {"success": True, "recipe": recipe}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.post("/find")
    async def find_recipes(request: FindRecipesRequest):
        """Find matching recipes from database"""
        try:
            recipes = await controller.find_matching_recipes(
                ingredients=request.ingredients,
                difficulty=request.difficulty,
                max_cooking_time=request.max_cooking_time,
                dietary_tags=request.dietary_tags
            )
            return {"success": True, "recipes": recipes, "count": len(recipes)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/{recipe_id}")
    async def get_recipe(recipe_id: str):
        """Get a specific recipe by ID"""
        try:
            recipe = await controller.get_recipe_by_id(recipe_id)
            if not recipe:
                raise HTTPException(status_code=404, detail="Recipe not found")
            return {"success": True, "recipe": recipe}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.post("/adjust-serving")
    async def adjust_serving(request: AdjustServingRequest):
        """Adjust recipe serving size"""
        try:
            recipe = await controller.adjust_serving_size(
                recipe_id=request.recipe_id,
                new_serving_size=request.new_serving_size
            )
            return {"success": True, "recipe": recipe}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    return router