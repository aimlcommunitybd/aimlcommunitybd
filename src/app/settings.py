# Configuration settings for the application
import os
import structlog
from dotenv import load_dotenv

load_dotenv()

logger = structlog.get_logger(__name__)

# Load env variables
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
DATABASE_DIR = os.getenv("DATABASE_DIR", ".data")
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATABASE_DIR}/database.db")
PORT = int(os.getenv("PORT", 10000))
BASE_DIR = os.getenv("BASE_DIR", "src/app/")
ACTIVITY_IMG_FOLDER = os.getenv("ACTIVITY_IMG_FOLDER", "assets/img/activities")
ADMIN_EMAIL=os.getenv("ADMIN_EMAIL", "admin@community.com")
ADMIN_PASSWORD=os.getenv("ADMIN_PASSWORD", "secret")

# DATABASE settings
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Img settings
ALLOWED_IMG_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_IMG_SIZE = 16 * 1024 * 1024  # 16MB max file size

# Create essential dirs
os.makedirs(DATABASE_DIR, exist_ok=True)

# logger.info(
#     f"Configuration loaded: DEBUG={DEBUG}, DATABASE_URL={DATABASE_URL}",
#     BASE_DIR=BASE_DIR,
#     ACTIVITY_IMG_FOLDER=ACTIVITY_IMG_FOLDER,
# )