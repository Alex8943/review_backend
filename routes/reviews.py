from typing import Optional, List, Dict
from bson.objectid import ObjectId
from db_services.connection import get_db_conn
from model.reviews_model import Review
from fastapi import APIRouter

db_conn = get_db_conn()
collection = db_conn.reviews
router = APIRouter()


@router.post("/review", response_model=Dict[str, str])
async def create_review(review: Review) -> Dict[str, str]:
    
    review_dict = review.dict()
    review_dict.pop('id', None)  # Remove 'id' if it exists because MongoDB generates it
    result = collection.insert_one(review_dict)
    return {'id': str(result.inserted_id)}


@router.get("/reviews", response_model=List[Review])
async def get_reviews() -> List[Review]:
    
    reviews = list(collection.find())
    for review in reviews:
        review["id"] = str(review["_id"])
        del review["_id"]
    return reviews


#Get a review by "title"
@router.get("/review/{title}", response_model=Review)
async def get_review(title: str) -> Review:
    
    review = collection.find_one({"title": title})
    review["id"] = str(review["_id"])
    del review["_id"]
    return review
