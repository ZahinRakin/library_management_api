from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from .db.db import connect_db, disconnect_db
from .api.book_routes import router as book_router

@asynccontextmanager
async def lifespan(app:FastAPI):

    load_dotenv()
    await connect_db()

    yield

    await disconnect_db()



app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.include_router(router=book_router, prefix="/api/v1/books", tags=["books"])
