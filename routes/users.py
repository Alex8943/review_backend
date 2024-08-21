
from typing import List, Dict
from bson.objectid import ObjectId
from db_services.connection import get_db_conn
from model.users_model import User
from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel
import os
import jwt
import bcrypt

db_conn = get_db_conn()
collection = db_conn.users
router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str

# Define a Pydantic model for the login request body
class LoginRequest(BaseModel):
    email: str
    password: str



def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



@router.post("/login", response_model=Token)
async def login_user(login: LoginRequest):
    user = collection.find_one({"email": login.email})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    if not bcrypt.checkpw(login.password.encode('utf-8'), user['password'].encode('utf-8')):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    # Create JWT token
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}



# Create a user with hashed password
@router.post("/user", response_model=Dict[str, str])
async def create_user(user: User) -> Dict[str, str]:
    # Hash the user's password
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    
    # plain text delete, hashed password saved
    user_dict = user.dict(by_alias=True)
    user_dict['password'] = hashed_password.decode('utf-8')  # Store as a string
    
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



# Delete a user with id
@router.delete("/user/{id}", response_model=Dict[str, str])
async def delete_user(id: str) -> Dict[str, str]:
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return {"message": "User with id: " + id + " deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User with id: " + id + " not found")
