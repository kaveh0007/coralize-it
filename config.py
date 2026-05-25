import os

class Config():
    GITHUB_API_BASE = os.environ.get("GITHUB_API_BASE") or "https://api.github.com"
    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")