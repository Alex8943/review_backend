from fastapi import FastAPI
from db_services.connection import get_db_conn
from fastapi.middleware.cors import CORSMiddleware
from routes.reviews import router as reviews_router
from routes.products import router as products_router
from routes.users import router as users_router


app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

#DB connection test
#db = get_db_conn()
#print("DB name: ", db.name)

app.include_router(reviews_router)
app.include_router(products_router)
app.include_router(users_router)
