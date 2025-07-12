from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os

from app.models.user_models import User

client: AsyncIOMotorClient | None = None  # Global client reference

async def connect_db():
    global client
    try:
        print("[DB] Connecting to MongoDB...")

        mongo_uri = os.getenv("MONGODB_URI")
        db_name = os.getenv("DB_NAME")

        if not mongo_uri or not db_name:
            raise ValueError("Environment variables MONGODB_URI and DB_NAME must be set.")

        client = AsyncIOMotorClient(mongo_uri)

        # Check MongoDB connection
        await client.admin.command("ping")
        print("[DB] Pinged MongoDB successfully.")

        db = client[db_name]

        # Initialize Beanie ODM
        await init_beanie(database=db, document_models=[User])
        print("[DB] Beanie initialized with User model.")

    except Exception as e:
        print(f"[DB] Failed to connect to MongoDB: {e}")

async def disconnect_db():
    global client
    if client:
        client.close()
        print("[DB] Disconnected from MongoDB.")
