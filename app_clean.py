from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_cors import CORS
from yoga_suggestions import suggest_yoga
from yoga_data import YOGA_POSES, MEDICINE_DATABASE
from models import db, User, Appointment
import os, random, time, logging, json
from datetime import datetime, date, timedelta
from functools import wraps

app = Flask(__name__)
app.secret_key = "healthcare_secret_2024_secure"

# Enable CORS for API endpoints
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure instance folder exists
instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
os.makedirs(instance_path, exist_ok=True)

# Use absolute path for database
db_path = os.path.join(instance_path, 'users.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

# ---------------- Reset tokens (in-memory for demo) ----------------
reset_tokens = {}    # {email: {"code": "123456", "expires": <epoch>}}

# --------------------------------- Authentication Helpers --------------------------------------

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login_register'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Get current logged-in user"""
    if 'user' in session:
        return User.query.filter_by(email=session['user']).first()
    return None

# --------------------------------- Helpers --------------------------------------

def compute_insights(mood, sleep, stress):
    """Return (score, condition, yoga_list, ayur_tip, allo_tip)."""
    mood_weights = {"calm": 85, "happy": 80, "ok": 65, "sad": 45, "tired": 40, "angry": 35}
    base = mood_weights.get(mood, 60)

    # sleep adjustment
    try:
        s = int(sleep)
    except:
        s = 7
    if 7 <= s <= 8:
        base += 15
    elif 6 <= s <= 9:
        base += 5
    elif s < 5 or s > 9:
        base -= 10

    # stress adjustment (1..10)
    try:
        st = int(stress)
    except:
        st = 4
    base -= (st - 3) * 5

    score = max(0, min(100, base))

    # focus area
    if st >= 7:
        condition = "stress"
    elif s <= 5:
        condition = "fatigue"
    elif mood in ("angry", "sad"):
        condition = "mental balance"
    else:
        condition = "general wellness"

    yoga_map = {
        "stress": ["Padmasana", "Shavasana", "Anulom Vilom"],
        "fatigue": ["Tadasana", "Balasana", "Viparita Karani"],
        "mental balance": ["Nadi Shodhana", "Bhramari", "Child's Pose"],
        "general wellness": ["Vajrasana", "Setu Bandhasana", "Cat-Cow Pose"],
    }
    ayur_map = {
        "stress": "Ashwagandha at night + 10 min meditation.",
        "fatigue": "Jeera–ajwain warm water + early light dinner.",
        "mental balance": "Brahmi tea + evening walk.",
        "general wellness": "Triphala (mild) + consistent bedtime.",
    }
    allo_map = {
        "stress": "B-complex once daily; limit caffeine; deep breathing.",
        "fatigue": "Hydration, electrolytes, and a short nap.",
        "mental balance": "Mindfulness 10 min; consult if persistent.",
        "general wellness": "Multivitamin (std. dose) & 30-min walk.",
    }

    return int(score), condition, yoga_map[condition], ayur_map[condition], allo_map[condition]

# --------------------------------- Auth & Account --------------------------------

@app.route("/")
def root():
    return redirect(url_for("login_register"))

@app.route("/login_register", methods=["GET", "POST"])
def login_register():
    msg = ""
    if request.method == "POST":
        action = (request.form.get("action") or "").strip().lower()
        email = (request.form.get("email") or "").strip().lower()
        password = (request.form.get("password") or "").strip()

        if action == "register":
            if not email or not password:
                msg = "Please enter both email and password."
            else:
                # Check if user already exists
                existing_user = User.query.filter_by(email=email).first()
                if existing_user:
                    msg = "User already exists!"
                else:
                    # Create new user with hashed password
                    new_user = User(email=email)
                    new_user.set_password(password)
                    db.session.add(new_user)
                    db.session.commit()
                    msg = "Registered successfully! Please log in."
        elif action == "login":
            # Find user in database
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session["user"] = email
                return redirect(url_for("home"))
            else:
                msg = "Invalid credentials!"
    return render_template("login_register.html", msg=msg, brand="Health Care")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login_register"))

# ---------- Forgot / Reset Password (demo: shows code on screen; no email needed) ----------

@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    info = ""
    code_generated = None
    email_entered = ""
    if request.method == "POST":
        email_entered = (request.form.get("email") or "").strip().lower()
        if not email_entered:
            info = "Please enter your email."
        else:
            # Check if user exists in database
            user = User.query.filter_by(email=email_entered).first()
            if not user:
                info = "No account found with that email."
            else:
                code_generated = f"{random.randint(0, 999999):06d}"
                reset_tokens[email_entered] = {
                    "code": code_generated,
                    "expires": time.time() + 15 * 60  # 15 minutes
                }
                info = "Reset code generated. Use it within 15 minutes."
    return render_template("forgot.html", info=info, code=code_generated, email=email_entered, brand="Health Care")

@app.route("/reset", methods=["GET", "POST"])
def reset():
    msg = ""
    success = False
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        code = (request.form.get("code") or "").strip()
        new_pwd = (request.form.get("new_password") or "").strip()
        confirm = (request.form.get("confirm_password") or "").strip()

        if not (email and code and new_pwd and confirm):
            msg = "Please fill all fields."
        elif new_pwd != confirm:
            msg = "Passwords do not match."
        elif email not in reset_tokens:
            msg = "No reset request found for this email. Please generate a code first."
        else:
            saved = reset_tokens[email]
            if time.time() > saved["expires"]:
                reset_tokens.pop(email, None)
                msg = "Reset code expired. Please generate a new code."
            elif code != saved["code"]:
                msg = "Invalid code."
            else:
                # Find user in database
                user = User.query.filter_by(email=email).first()
                if not user:
                    msg = "Account not found."
                else:
                    # Update password with hashing
                    user.set_password(new_pwd)
                    db.session.commit()
                    reset_tokens.pop(email, None)
                    success = True
                    msg = "Password updated. You can now log in."
    return render_template("reset.html", msg=msg, success=success, brand="Health Care")

# --------------------------------- Main Pages -----------------------------------

@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login_register"))
    return render_template("home.html", user=session["user"], brand="Health Care")

if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)