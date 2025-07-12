from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os

from app.models.loan_extension_models import LoanExtension
from app.models.loan_models import Loan

client = None  # Motor client (global)

async def connect_db():
    global client
    try:
        print("[DB] Connecting to MongoDB...")

        # Load env vars
        mongo_uri = os.getenv("MONGODB_URI")
        db_name = os.getenv("DB_NAME")

        if not mongo_uri or not db_name:
            raise ValueError("MONGODB_URI and DB_NAME must be set in environment variables.")

        # Async MongoDB client
        client = AsyncIOMotorClient(mongo_uri)

        # Test connection
        await client.admin.command("ping")
        print("[DB] Ping successful. Connected to MongoDB.")

        # Connect to specified database and initialize Beanie
        db = client[db_name]
        await init_beanie(database=db, document_models=[Loan, LoanExtension])

        print("[DB] Beanie initialized with models: Loan, LoanExtension")

    except Exception as e:
        print(f"[DB] Failed to connect to MongoDB: {e}")

async def disconnect_db():
    global client
    if client:
        client.close()
        print("[DB] Disconnected from MongoDB.")
