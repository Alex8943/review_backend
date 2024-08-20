from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId


class Review(BaseModel):
    id: Optional[str] = Field(None, alias="id")
    title: str #product_id
    description: str


    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


