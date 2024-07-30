from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class Review(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    title: str
    description: str
    rating: int = Field(..., ge=1, le=5)
    user_id: Optional[str] = None
    product_id: Optional[str] = None  
    created_at: Optional[str] = None  # ISO format date-time string
    updated_at: Optional[str] = None  # ISO format date-time string

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True  # Allow custom data types like ObjectId
        json_encoders = {
            ObjectId: str  # Encode ObjectId as string in JSON
        }

