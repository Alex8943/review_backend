from fastapi import FastAPI
from db_services.connection import get_db_conn

from routes.reviews import router as reviews_router

app = FastAPI()

#DB connection test
#db = get_db_conn()
#print("DB name: ", db.name)

app.include_router(reviews_router)


