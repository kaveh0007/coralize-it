from flask import Flask
from config import Config
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("WARNING: GEMINI_API_KEY not set. API features will fail.")
    client = None
else:
    client = genai.Client(api_key=api_key)

from app import routes