import os
import time
import logging
import threading
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt

# -----------------------------
# LOGGING
# -----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# -----------------------------
# FLASK APP
# -----------------------------
app = Flask(__name__)
CORS(app)

# -----------------------------
# DATABASE
# -----------------------------
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DATABASE_NAME", "facerecognition")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app.config["DB"] = db

bcrypt = Bcrypt(app)

# -----------------------------
# LIGHTWEIGHT MODEL MANAGER (FIXED)
# -----------------------------
class ModelManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def initialize(self):
        """Lazy load models (ONLY when needed)"""
        if self.initialized:
            return

        try:
            logger.info("⚡ Lazy loading models...")

            from mtcnn import MTCNN
            from deepface import DeepFace
            import numpy as np

            self.detector = MTCNN()

            # quick warmup (light)
            dummy = np.zeros((160, 160, 3), dtype=np.uint8)
            DeepFace.represent(
                dummy,
                model_name="Facenet512",
                detector_backend="skip",
                enforce_detection=False
            )

            self.initialized = True
            logger.info("✅ Models loaded successfully")

        except Exception as e:
            logger.error(f"❌ Model loading failed: {e}")
            raise e

    def get_detector(self):
        self.initialize()
        return self.detector


model_manager = ModelManager()

# -----------------------------
# ROUTES (IMPORTANT)
# -----------------------------

@app.route("/")
def home():
    return "Face Recognition Backend Running ✅"

@app.route("/health")
def health():
    return {
        "status": "ok",
        "time": time.time()
    }

# -----------------------------
# BLUEPRINTS (SAFE LOAD)
# -----------------------------
try:
    from auth.routes import auth_bp
    app.register_blueprint(auth_bp)
    logger.info("✅ Auth routes loaded")
except Exception as e:
    logger.warning(f"Auth routes error: {e}")

try:
    from student.registration import student_registration_bp
    app.register_blueprint(student_registration_bp)
except:
    pass

try:
    from student.updatedetails import student_update_bp
    app.register_blueprint(student_update_bp)
except:
    pass

try:
    from student.demo_session import demo_session_bp
    app.register_blueprint(demo_session_bp)
except:
    pass

try:
    from student.view_attendance import attendance_bp
    app.register_blueprint(attendance_bp)
except:
    pass

try:
    from teacher.attendance_records import attendance_session_bp
    app.register_blueprint(attendance_session_bp)
except:
    pass

# -----------------------------
# IMPORTANT: RENDER PORT FIX
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    logger.info(f"🚀 Starting server on port {port}")
    app.run(host="0.0.0.0", port=port)
