from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os

from librarymanagement.models.loan_extension_models import LoanExtension
from librarymanagement.models.user_models import User
from librarymanagement.models.loan_models import Loan
from librarymanagement.models.book_models import Book


client = None  # Declare client outside to use it for both connect and disconnect

async def connect_db():
    global client
    try:
        print("connecting to database")  # debugging log
        client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
        db = client[os.getenv("DB_NAME")]
        await init_beanie(db, document_models=[User, Loan, LoanExtension, Book])
        print("database connected")     # debugging log
    except Exception as e:
        print(f"something happened while connecting to the database. \n{e}")

async def disconnect_db():
    global client
    if client:
        client.close()  # Close the connection
        print("Disconnected from the database.")
