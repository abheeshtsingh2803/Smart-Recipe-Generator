from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone

class NutritionInfo(BaseModel):
    calories: int
    protein: int
    carbs: int
    fat: int
    fiber: Optional[int] = 0

class Recipe(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    ingredients: List[str]
    instructions: List[str]
    cuisine: str
    difficulty: str  # easy, medium, hard
    cooking_time: int  # in minutes
    serving_size: int
    dietary_tags: List[str]  # vegetarian, vegan, gluten-free, etc.
    nutrition: NutritionInfo
    image_url: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class RecipeCreate(BaseModel):
    name: str
    ingredients: List[str]
    instructions: List[str]
    cuisine: str
    difficulty: str
    cooking_time: int
    serving_size: int
    dietary_tags: List[str]
    nutrition: NutritionInfo
    image_url: Optional[str] = None