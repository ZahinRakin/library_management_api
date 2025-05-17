from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from app.db.db import connect_db, disconnect_db
from app.api.user_routes import router as user_router

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

app.include_router(router=user_router, prefix="/api/v1/users", tags=["users"])
