import os
from dotenv import load_dotenv

load_dotenv()

USAJOBS_API_KEY = os.getenv("USAJOBS_API_KEY")
USAJOBS_EMAIL = os.getenv("USAJOBS_EMAIL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
