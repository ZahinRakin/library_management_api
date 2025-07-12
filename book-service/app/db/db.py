from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os
from app.models.book_models import Book

client = None  # Motor client (async)
db = None      # database handle

async def connect_db():
    global client, db
    try:
        print("connecting to database")  # debugging log

        uri = os.getenv("MONGODB_URI")
        client = AsyncIOMotorClient(uri)

        # Ping the server (Motor's syntax is async)
        await client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")

        db_name = os.getenv("DB_NAME")
        db = client[db_name]

        # Now pass Motor client’s database to Beanie
        await init_beanie(database=db, document_models=[Book])
        print("database connected")
    except Exception as e:
        print(f"something happened while connecting to the database. \n{e}")

async def disconnect_db():
    global client
    if client:
        client.close()
        print("Disconnected from the database.")
