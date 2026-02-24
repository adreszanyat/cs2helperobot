import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "1210142965").split(",")))

if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
    raise ValueError("BOT_TOKEN не настроен в .env файле!")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MEDIA_DIR = os.path.join(BASE_DIR, "media")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(os.path.join(MEDIA_DIR, "nades"), exist_ok=True)
os.makedirs(os.path.join(MEDIA_DIR, "crosshairs"), exist_ok=True)
os.makedirs(os.path.join(MEDIA_DIR, "sprays"), exist_ok=True)
os.makedirs(os.path.join(MEDIA_DIR, "configs"), exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, "cs2_bot.db")

MAX_FAVORITES_PER_USER = 50
SUPPORTED_MAPS = ["mirage", "inferno", "nuke", "ancient", "anubis", "vertigo", "overpass", "dust2"]
NADE_TYPES = ["smoke", "flash", "molotov", "he"]