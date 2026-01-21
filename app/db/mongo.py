from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

if not MONGO_URL:
    raise ValueError("MONGO_URL is not set .env file")

client = MongoClient(MONGO_URL)

try:
    client.admin.command("ping")
    print("MongoDB is connected")
except Exception as e:
    print("MongoDB connection failed")
    print(e)

db = client["Ai_chatboat"]
session_collection =db["sessions"]
chat_collection = db["chats"]
soap_collection = db["soap_reports"]

