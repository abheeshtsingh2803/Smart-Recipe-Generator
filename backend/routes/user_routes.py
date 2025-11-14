from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from controllers.user_controller import UserController
from models.user_preference import UserPreferenceCreate
from models.saved_recipe import SavedRecipeCreate

router = APIRouter(prefix="/user", tags=["user"])

def init_user_routes(db: AsyncIOMotorDatabase):
    controller = UserController(db)
    
    @router.post("/preferences")
    async def save_preferences(preferences: UserPreferenceCreate):
        """Save or update user preferences"""
        try:
            result = await controller.save_user_preferences(preferences)
            return {"success": True, "preferences": result}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/preferences/{user_session}")
    async def get_preferences(user_session: str):
        """Get user preferences"""
        try:
            prefs = await controller.get_user_preferences(user_session)
            return {"success": True, "preferences": prefs}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.post("/saved-recipes")
    async def save_recipe(saved_recipe: SavedRecipeCreate):
        """Save a recipe to favorites"""
        try:
            result = await controller.save_recipe(saved_recipe)
            return {"success": True, "saved_recipe": result}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/saved-recipes/{user_session}")
    async def get_saved_recipes(user_session: str):
        """Get user's saved recipes"""
        try:
            recipes = await controller.get_saved_recipes(user_session)
            return {"success": True, "recipes": recipes, "count": len(recipes)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.delete("/saved-recipes/{user_session}/{recipe_id}")
    async def delete_saved_recipe(user_session: str, recipe_id: str):
        """Remove a recipe from favorites"""
        try:
            success = await controller.delete_saved_recipe(user_session, recipe_id)
            if not success:
                raise HTTPException(status_code=404, detail="Saved recipe not found")
            return {"success": True, "message": "Recipe removed from favorites"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    return router