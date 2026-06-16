import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DEBUG", "False").lower() == "true"
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "outputs")
TEMP_DIR = os.getenv("TEMP_DIR", "temp_videos")

# Ensure directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
