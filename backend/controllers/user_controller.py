from typing import List, Dict, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.user_preference import UserPreference, UserPreferenceCreate
from models.saved_recipe import SavedRecipe, SavedRecipeCreate
import logging

logger = logging.getLogger(__name__)

class UserController:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def save_user_preferences(self, preferences: UserPreferenceCreate) -> Dict:
        """Save or update user preferences"""
        try:
            # Check if preferences exist for this session
            existing = await self.db.user_preferences.find_one(
                {"user_session": preferences.user_session},
                {"_id": 0}
            )
            
            if existing:
                # Update existing
                await self.db.user_preferences.update_one(
                    {"user_session": preferences.user_session},
                    {"$set": preferences.model_dump()}
                )
                return {**existing, **preferences.model_dump()}
            else:
                # Create new
                pref_obj = UserPreference(**preferences.model_dump())
                doc = pref_obj.model_dump()
                doc['created_at'] = doc['created_at'].isoformat()
                await self.db.user_preferences.insert_one(doc)
                return doc
        except Exception as e:
            logger.error(f"Error saving preferences: {str(e)}")
            raise
    
    async def get_user_preferences(self, user_session: str) -> Optional[Dict]:
        """Get user preferences"""
        try:
            prefs = await self.db.user_preferences.find_one(
                {"user_session": user_session},
                {"_id": 0}
            )
            return prefs
        except Exception as e:
            logger.error(f"Error getting preferences: {str(e)}")
            raise
    
    async def save_recipe(self, saved_recipe: SavedRecipeCreate) -> Dict:
        """Save a recipe to user's favorites"""
        try:
            # Check if already saved
            existing = await self.db.saved_recipes.find_one(
                {
                    "user_session": saved_recipe.user_session,
                    "recipe_id": saved_recipe.recipe_id
                },
                {"_id": 0}
            )
            
            if existing:
                # Update rating/notes
                await self.db.saved_recipes.update_one(
                    {
                        "user_session": saved_recipe.user_session,
                        "recipe_id": saved_recipe.recipe_id
                    },
                    {"$set": {"rating": saved_recipe.rating, "notes": saved_recipe.notes}}
                )
                return {**existing, "rating": saved_recipe.rating, "notes": saved_recipe.notes}
            else:
                # Create new
                saved_obj = SavedRecipe(**saved_recipe.model_dump())
                doc = saved_obj.model_dump()
                doc['created_at'] = doc['created_at'].isoformat()
                await self.db.saved_recipes.insert_one(doc)
                return doc
        except Exception as e:
            logger.error(f"Error saving recipe: {str(e)}")
            raise
    
    async def get_saved_recipes(self, user_session: str) -> List[Dict]:
        """Get user's saved recipes with full recipe details"""
        try:
            saved = await self.db.saved_recipes.find(
                {"user_session": user_session},
                {"_id": 0}
            ).to_list(1000)
            
            # Fetch full recipe details for each saved recipe
            result = []
            for saved_recipe in saved:
                recipe = await self.db.recipes.find_one(
                    {"id": saved_recipe['recipe_id']},
                    {"_id": 0}
                )
                if recipe:
                    result.append({
                        **recipe,
                        "user_rating": saved_recipe.get('rating', 0),
                        "user_notes": saved_recipe.get('notes', '')
                    })
            
            return result
        except Exception as e:
            logger.error(f"Error getting saved recipes: {str(e)}")
            raise
    
    async def delete_saved_recipe(self, user_session: str, recipe_id: str) -> bool:
        """Remove a recipe from favorites"""
        try:
            result = await self.db.saved_recipes.delete_one({
                "user_session": user_session,
                "recipe_id": recipe_id
            })
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting saved recipe: {str(e)}")
            raise