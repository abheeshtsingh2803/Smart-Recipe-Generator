from typing import List
from services.openai_service import OpenAIService
import logging

logger = logging.getLogger(__name__)

class IngredientController:
    def __init__(self):
        self.openai_service = OpenAIService()
    
    async def recognize_ingredients_from_image(self, image_base64: str) -> List[str]:
        """Process image and recognize ingredients"""
        try:
            ingredients = await self.openai_service.recognize_ingredients_from_image(image_base64)
            return ingredients
        except Exception as e:
            logger.error(f"Error recognizing ingredients: {str(e)}")
            raise