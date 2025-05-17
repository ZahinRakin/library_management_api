from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os

from app.models.user_models import User


client = None  # Declare client outside to use it for both connect and disconnect

async def connect_db():
    global client
    try:
        print("connecting to database")  # debugging log
        client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
        db = client[os.getenv("DB_NAME")]
        await init_beanie(db, document_models=[User ])
        print("database connected")     # debugging log
    except Exception as e:
        print(f"something happened while connecting to the database. \n{e}")

async def disconnect_db():
    global client
    if client:
        client.close()  # Close the connection
        print("Disconnected from the database.")
