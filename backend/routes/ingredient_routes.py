from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from controllers.ingredient_controller import IngredientController

router = APIRouter(prefix="/ingredients", tags=["ingredients"])

class RecognizeImageRequest(BaseModel):
    image_base64: str

def init_ingredient_routes():
    controller = IngredientController()
    
    @router.post("/recognize")
    async def recognize_ingredients(request: RecognizeImageRequest):
        """Recognize ingredients from an uploaded image"""
        try:
            ingredients = await controller.recognize_ingredients_from_image(request.image_base64)
            return {"success": True, "ingredients": ingredients}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    return router