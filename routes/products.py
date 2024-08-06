from typing import Optional, List, Dict
from bson.objectid import ObjectId
from db_services.connection import get_db_conn
from model.products_model import Product
from fastapi import APIRouter

db_conn = get_db_conn()
collection = db_conn.products
router = APIRouter()

#create a product
@router.post("/product", response_model=Dict[str, str])
async def create_product(product: Product) -> Dict[str, str]:
    
    product_dict = product.dict(by_alias=True)
    result = collection.insert_one(product_dict)
    return {'id': str(result.inserted_id)}


# Get all products
@router.get("/products", response_model=List[Product])
async def get_products() -> List[Product]:
    products = list(collection.find())
    for product in products:
        product["id"] = str(product["_id"])
        del product["_id"]
    return products




