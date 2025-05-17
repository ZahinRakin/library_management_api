from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import os

from librarymanagement.db.connectDB import connect_db, disconnect_db
from librarymanagement.routes.user_routes import router as user_router
from librarymanagement.routes.book_routes import router as book_router
from librarymanagement.routes.loan_routes import router as loan_router
from librarymanagement.routes.stat_routes import router as stat_router

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

app.include_router(router=user_router, prefix="/api/users", tags=["users"])
app.include_router(router=book_router, prefix="/api/books", tags=["books"])
app.include_router(router=loan_router, prefix="/api/loans", tags=["loans"])
app.include_router(router=stat_router, prefix="/api/stats", tags=["stats"])


