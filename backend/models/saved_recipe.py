from pydantic import BaseModel, Field, ConfigDict
import uuid
from datetime import datetime, timezone

class SavedRecipe(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_session: str
    recipe_id: str
    rating: int = 0  # 1-5 stars
    notes: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class SavedRecipeCreate(BaseModel):
    user_session: str
    recipe_id: str
    rating: int = 0
    notes: str = ""