# Configuration settings for the application
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")
PORT = int(os.getenv("PORT", 10000))

BASE_DIR = os.getenv("BASE_DIR", "src/app/")
ACTIVITY_IMG_FOLDER = os.getenv("ACTIVITY_IMG_FOLDER", "assets/img/activities")
ALLOWED_IMG_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_IMG_SIZE = 16 * 1024 * 1024  # 16MB max file size

ADMIN_EMAIL=os.environ.get("ADMIN_EMAIL", "admin@community.com")
ADMIN_PASSWORD=os.environ.get("ADMIN_PASSWORD", "secret")