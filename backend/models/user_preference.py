from pydantic import BaseModel, Field, ConfigDict
from typing import List
import uuid
from datetime import datetime, timezone

class UserPreference(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_session: str  # Simple session-based user tracking
    dietary_restrictions: List[str] = []
    favorite_cuisines: List[str] = []
    allergies: List[str] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserPreferenceCreate(BaseModel):
    user_session: str
    dietary_restrictions: List[str] = []
    favorite_cuisines: List[str] = []
    allergies: List[str] = []