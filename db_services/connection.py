from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()

def get_db_conn(): 
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client.reviews

    return db



