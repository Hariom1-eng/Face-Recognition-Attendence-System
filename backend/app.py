import os
import time
import logging
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
# ROUTES
# -----------------------------
@app.route("/")
def home():
    return "Backend Running ✅"

@app.route("/health")
def health():
    return {"status": "ok", "time": time.time()}

# -----------------------------
# BLUEPRINTS (DELAYED IMPORT)
# -----------------------------

def register_blueprints():
    try:
        from auth.routes import auth_bp
        app.register_blueprint(auth_bp)
        logger.info("Auth loaded")
    except Exception as e:
        logger.warning(e)

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


# Call AFTER app creation (lazy)
register_blueprints()

# -----------------------------
# IMPORTANT: RENDER PORT FIX
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    logger.info(f"🚀 Running on port {port}")
    app.run(host="0.0.0.0", port=port)
