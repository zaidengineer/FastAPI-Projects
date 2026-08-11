from fastapi import FastAPI

from database import engine, Base
from models import User
from routers.auth import router as auth_router
from users import router as users_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Authentication API",
    version="1.0.0"
)

from fastapi.middleware.cors import CORSMiddleware


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:3000",
        "http://localhost:3000",

        "http://127.0.0.1:3002",
        "http://localhost:3002",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(users_router)


@app.get("/")
def home():
    return {
        "message": "Authentication API is running"
    }