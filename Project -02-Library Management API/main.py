from fastapi import FastAPI

from routers.book import router as book_router
from routers.user import router as user_router
from routers.borrow import router as borrow_router

app = FastAPI(
    title="Library Management API",
    version="1.0"
)

app.include_router(book_router)
app.include_router(user_router)
app.include_router(borrow_router)