from motor.motor_asyncio import AsyncIOMotorClient
from typing import AsyncGenerator

from dotenv import load_dotenv
import os
import urllib.parse

load_dotenv()

username = os.getenv("DB_USERNAME")
password = urllib.parse.quote_plus(os.getenv("DB_PASSWORD"))  # Safe encoding
db_name = os.getenv("DB_NAME")

MONGO_URI = f"mongodb+srv://{username}:{password}@hyphen200.mslpw3w.mongodb.net/{db_name}?retryWrites=true&w=majority&tls=true"

client = AsyncIOMotorClient(MONGO_URI, tls=True)

db = client[db_name]

user_collection = db.user
chat_collection = db.chat

async def get_database() -> AsyncGenerator:
    yield db
