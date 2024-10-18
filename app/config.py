from datetime import timedelta
import os
from dotenv import load_dotenv


load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
DB_URL = os.getenv("DB_URL")
ALGORITHM = os.getenv("ALGORITHM")
DEFAULT_EXPIRED_TIME = timedelta(minutes=30)