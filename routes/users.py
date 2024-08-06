from typing import List, Dict
from bson.objectid import ObjectId
from db_services.connection import get_db_conn
from model.users_model import User
from fastapi import APIRouter, HTTPException

db_conn = get_db_conn()
collection = db_conn.users
router = APIRouter()

# Create a user
@router.post("/user", response_model=Dict[str, str])
async def create_user(user: User) -> Dict[str, str]:
    user_dict = user.dict(by_alias=True)
    result = collection.insert_one(user_dict)
    return {'id': str(result.inserted_id)}

# Get all users
@router.get("/users", response_model=List[User])
async def get_users() -> List[User]:
    users = list(collection.find())
    for user in users:
        user["id"] = str(user["_id"])
        del user["_id"]
    return users

#Delete a user with id
#How to delete a user, with an id that is null??
@router.delete("/user/{id}", response_model=Dict[str, str])
async def delete_user(id: str) -> Dict[str, str]:
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return {"message": "User with id: " + id + " deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User with id: " + id + " not found")
