import os
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME", "anon_session")

if not API_ID or not API_HASH:
    raise ValueError("❌ Error: API_ID or API_HASH not found in .env file")

API_ID = int(API_ID)
