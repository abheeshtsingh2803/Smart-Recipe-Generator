from emergentintegrations.llm.chat import LlmChat, UserMessage, ImageContent
import os
from typing import List, Dict
import logging
import base64
from pathlib import Path

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.api_key = os.environ.get('EMERGENT_LLM_KEY')
        if not self.api_key:
            raise ValueError("EMERGENT_LLM_KEY not found in environment")
    
    async def recognize_ingredients_from_image(self, image_base64: str) -> List[str]:
        """Recognize ingredients from an image using GPT-4 Vision"""
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"ingredient_recognition",
                system_message="You are an expert chef and ingredient recognition assistant. Analyze images and identify all visible ingredients with high accuracy."
            ).with_model("openai", "gpt-4o")
            
            image_content = ImageContent(image_base64=image_base64)
            
            user_message = UserMessage(
                text="Please identify all the ingredients visible in this image. List them clearly, one per line. Only list the ingredient names, nothing else.",
                file_contents=[image_content]
            )
            
            response = await chat.send_message(user_message)
            
            # Parse the response to extract ingredients
            ingredients = [line.strip() for line in response.split('\n') if line.strip() and not line.strip().startswith('#')]
            
            return ingredients
            
        except Exception as e:
            logger.error(f"Error recognizing ingredients: {str(e)}")
            raise
    
    async def generate_recipe(self, ingredients: List[str], dietary_preferences: List[str] = [], 
                             cuisine_preference: str = None, difficulty: str = None) -> Dict:
        """Generate a recipe using available ingredients"""
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"recipe_generation",
                system_message="You are a professional chef and recipe creator. Generate creative, delicious, and practical recipes based on available ingredients."
            ).with_model("openai", "gpt-4o")
            
            prompt = f"""Create a detailed recipe using these ingredients: {', '.join(ingredients)}
            
{'Dietary preferences: ' + ', '.join(dietary_preferences) if dietary_preferences else ''}
{'Preferred cuisine: ' + cuisine_preference if cuisine_preference else ''}
{'Difficulty level: ' + difficulty if difficulty else ''}

Provide the recipe in the following EXACT format:

NAME: [Recipe Name]
CUISINE: [Cuisine Type]
DIFFICULTY: [easy/medium/hard]
COOKING_TIME: [time in minutes, number only]
SERVING_SIZE: [number of servings, number only]
DIETARY_TAGS: [comma-separated tags like vegetarian, vegan, gluten-free]

INGREDIENTS:
- [ingredient 1 with quantity]
- [ingredient 2 with quantity]
...

INSTRUCTIONS:
1. [step 1]
2. [step 2]
...

NUTRITION (per serving):
Calories: [number]
Protein: [number]g
Carbs: [number]g
Fat: [number]g
Fiber: [number]g
"""
            
            user_message = UserMessage(text=prompt)
            response = await chat.send_message(user_message)
            
            # Parse the response into structured data
            recipe_data = self._parse_recipe_response(response)
            return recipe_data
            
        except Exception as e:
            logger.error(f"Error generating recipe: {str(e)}")
            raise
    
    def _parse_recipe_response(self, response: str) -> Dict:
        """Parse the AI response into structured recipe data"""
        lines = response.split('\n')
        recipe = {
            'name': '',
            'cuisine': '',
            'difficulty': 'medium',
            'cooking_time': 30,
            'serving_size': 4,
            'dietary_tags': [],
            'ingredients': [],
            'instructions': [],
            'nutrition': {
                'calories': 0,
                'protein': 0,
                'carbs': 0,
                'fat': 0,
                'fiber': 0
            }
        }
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith('NAME:'):
                recipe['name'] = line.split(':', 1)[1].strip()
            elif line.startswith('CUISINE:'):
                recipe['cuisine'] = line.split(':', 1)[1].strip()
            elif line.startswith('DIFFICULTY:'):
                recipe['difficulty'] = line.split(':', 1)[1].strip().lower()
            elif line.startswith('COOKING_TIME:'):
                try:
                    recipe['cooking_time'] = int(''.join(filter(str.isdigit, line.split(':', 1)[1])))
                except:
                    recipe['cooking_time'] = 30
            elif line.startswith('SERVING_SIZE:'):
                try:
                    recipe['serving_size'] = int(''.join(filter(str.isdigit, line.split(':', 1)[1])))
                except:
                    recipe['serving_size'] = 4
            elif line.startswith('DIETARY_TAGS:'):
                tags = line.split(':', 1)[1].strip()
                recipe['dietary_tags'] = [tag.strip() for tag in tags.split(',') if tag.strip()]
            elif line.startswith('INGREDIENTS:'):
                current_section = 'ingredients'
            elif line.startswith('INSTRUCTIONS:'):
                current_section = 'instructions'
            elif line.startswith('NUTRITION'):
                current_section = 'nutrition'
            elif current_section == 'ingredients' and (line.startswith('-') or line.startswith('•')):
                recipe['ingredients'].append(line.lstrip('-•').strip())
            elif current_section == 'instructions' and line[0].isdigit():
                recipe['instructions'].append(line.split('.', 1)[1].strip() if '.' in line else line)
            elif current_section == 'nutrition':
                if 'Calories:' in line:
                    try:
                        recipe['nutrition']['calories'] = int(''.join(filter(str.isdigit, line.split(':', 1)[1])))
                    except:
                        pass
                elif 'Protein:' in line:
                    try:
                        recipe['nutrition']['protein'] = int(''.join(filter(str.isdigit, line.split(':', 1)[1])))
                    except:
                        pass
                elif 'Carbs:' in line:
                    try:
                        recipe['nutrition']['carbs'] = int(''.join(filter(str.isdigit, line.split(':', 1)[1])))
                    except:
                        pass
                elif 'Fat:' in line:
                    try:
                        recipe['nutrition']['fat'] = int(''.join(filter(str.isdigit, line.split(':', 1)[1])))
                    except:
                        pass
                elif 'Fiber:' in line:
                    try:
                        recipe['nutrition']['fiber'] = int(''.join(filter(str.isdigit, line.split(':', 1)[1])))
                    except:
                        pass
        
        return recipe