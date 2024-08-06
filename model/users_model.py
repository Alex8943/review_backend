from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class User(BaseModel):
    id: Optional[str] = Field(None, alias="id")
    name: str
    lastname: str
    email: str
    password: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
