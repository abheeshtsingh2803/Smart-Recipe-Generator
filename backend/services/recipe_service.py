from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class RecipeMatchingService:
    @staticmethod
    def calculate_match_score(recipe_ingredients: List[str], available_ingredients: List[str]) -> float:
        """Calculate how well a recipe matches available ingredients"""
        if not recipe_ingredients:
            return 0.0
        
        # Normalize ingredient names for better matching
        available_normalized = [ing.lower().strip() for ing in available_ingredients]
        
        matches = 0
        for recipe_ing in recipe_ingredients:
            recipe_ing_normalized = recipe_ing.lower().strip()
            # Check if any available ingredient is mentioned in the recipe ingredient
            for avail_ing in available_normalized:
                if avail_ing in recipe_ing_normalized or recipe_ing_normalized in avail_ing:
                    matches += 1
                    break
        
        score = (matches / len(recipe_ingredients)) * 100
        return round(score, 2)
    
    @staticmethod
    def filter_recipes_by_criteria(
        recipes: List[Dict], 
        difficulty: str = None,
        max_cooking_time: int = None,
        dietary_tags: List[str] = None,
        min_match_score: float = 0
    ) -> List[Dict]:
        """Filter recipes based on various criteria"""
        filtered = recipes
        
        if difficulty:
            filtered = [r for r in filtered if r.get('difficulty', '').lower() == difficulty.lower()]
        
        if max_cooking_time:
            filtered = [r for r in filtered if r.get('cooking_time', 999) <= max_cooking_time]
        
        if dietary_tags:
            dietary_tags_lower = [tag.lower() for tag in dietary_tags]
            filtered = [
                r for r in filtered 
                if any(tag.lower() in dietary_tags_lower for tag in r.get('dietary_tags', []))
            ]
        
        if min_match_score > 0:
            filtered = [r for r in filtered if r.get('match_score', 0) >= min_match_score]
        
        return filtered
    
    @staticmethod
    def suggest_substitutions(missing_ingredients: List[str]) -> Dict[str, List[str]]:
        """Suggest substitutions for missing ingredients"""
        substitution_map = {
            'butter': ['margarine', 'coconut oil', 'olive oil'],
            'milk': ['almond milk', 'soy milk', 'coconut milk', 'oat milk'],
            'egg': ['flax egg', 'chia egg', 'applesauce', 'banana'],
            'flour': ['almond flour', 'coconut flour', 'rice flour'],
            'sugar': ['honey', 'maple syrup', 'agave nectar', 'stevia'],
            'cream': ['coconut cream', 'cashew cream', 'greek yogurt'],
            'cheese': ['nutritional yeast', 'cashew cheese', 'tofu'],
        }
        
        suggestions = {}
        for ingredient in missing_ingredients:
            ingredient_lower = ingredient.lower()
            for key, subs in substitution_map.items():
                if key in ingredient_lower:
                    suggestions[ingredient] = subs
                    break
        
        return suggestions