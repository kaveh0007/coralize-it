from flask import Flask
from config import Config
from google import genai
import os

app = Flask(__name__)
app.config.from_object(Config)

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

from app import routes