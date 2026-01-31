from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_cors import CORS
from yoga_suggestions import suggest_yoga
from yoga_data import YOGA_POSES, MEDICINE_DATABASE
from models import db, User, Appointment
import os, random, time, logging, json
from datetime import datetime, date, timedelta
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "healthcare_secret_2024_secure")

# Enable CORS for API endpoints
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure instance folder exists
instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
os.makedirs(instance_path, exist_ok=True)

# Use absolute path for database - modified for Vercel deployment
if os.environ.get('VERCEL'):
    # For Vercel deployment, use a temporary database (consider using external DB for production)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/users.db'
else:
    # Local development
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
@login_required
def home():
    return render_template("home.html", user=session["user"], brand="Health Care")

@app.route("/appointments")
@login_required
def appointments():
    """View all appointments for logged-in user"""
    user_email = session["user"]
    user_appointments = Appointment.query.filter_by(patient_email=user_email).order_by(Appointment.appointment_date.desc()).all()
    
    return render_template("appointments.html", appointments=user_appointments, brand="Health Care")

@app.route("/consult")
@login_required
def consult():
    return render_template("consult.html", brand="Health Care")

@app.route("/yoga", methods=["GET", "POST"])
@login_required
def yoga():
    poses = []
    pose_details = []
    disease = ""
    if request.method == "POST":
        disease = (request.form.get("disease") or "").strip()
        if disease:
            poses = suggest_yoga(disease)
            # Get detailed information for each pose
            for pose in poses:
                # Extract just the pose name (before parenthesis)
                pose_key = pose.split("(")[0].strip()
                if pose_key in YOGA_POSES:
                    pose_details.append({
                        "key": pose_key,
                        "data": YOGA_POSES[pose_key]
                    })
            # Increment yoga session counter
            session["yoga_sessions"] = session.get("yoga_sessions", 0) + 1
    return render_template("yoga.html", poses=poses, pose_details=pose_details, disease=disease, brand="Health Care")

@app.route("/yoga/<pose_name>")
@login_required
def yoga_detail(pose_name):
    """Detailed view for a specific yoga pose"""
    pose = YOGA_POSES.get(pose_name)
    if not pose:
        return redirect(url_for("yoga"))
    
    return render_template("yoga_detail.html", pose=pose, pose_name=pose_name, brand="Health Care")

@app.route("/allopathic", methods=["GET", "POST"])
@login_required
def allopathic():
    suggestion = None
    medicine_details = None
    disease = ""
    allopathy_map = {
        "fever": {"text": "Paracetamol 500 mg — 1 tablet every 8 hours after food", "medicine": "paracetamol"},
        "cold": {"text": "Cetirizine 10 mg — once at night", "medicine": "cetirizine"},
        "headache": {"text": "Paracetamol 500 mg — as needed after food", "medicine": "paracetamol"},
        "back pain": {"text": "Ibuprofen 400 mg — twice daily + local heat", "medicine": "ibuprofen"},
        "asthma": {"text": "Salbutamol inhaler — 2 puffs as needed", "medicine": None},
        "diabetes": {"text": "Metformin 500 mg — morning & night with food", "medicine": "metformin"},
        "stress": {"text": "Vitamin B-complex — once daily", "medicine": None},
    }
    if request.method == "POST":
        disease = (request.form.get("disease") or "").lower().strip()
        result = allopathy_map.get(disease)
        if result:
            suggestion = result["text"]
            if result["medicine"] and result["medicine"] in MEDICINE_DATABASE:
                medicine_details = MEDICINE_DATABASE[result["medicine"]]
        else:
            suggestion = "No ready suggestion found. Please consult a doctor."
        # Increment allopathic counter
        session["allopathic_count"] = session.get("allopathic_count", 0) + 1
    return render_template("allopathic.html", disease=disease, suggestion=suggestion, medicine_details=medicine_details, brand="Health Care")

@app.route("/medicine/<medicine_name>")
@login_required
def medicine_detail(medicine_name):
    """Detailed view for a specific medicine"""
    medicine = MEDICINE_DATABASE.get(medicine_name)
    if not medicine:
        return redirect(url_for("allopathic"))
    
    return render_template("medicine_detail.html", medicine=medicine, medicine_name=medicine_name, brand="Health Care")

@app.route("/ayurvedic", methods=["GET", "POST"])
@login_required
def ayurvedic():
    remedy = None
    disease = ""
    ayur_map = {
        "fever": "Tulsi + Ginger Kadha — twice daily",
        "cold": "Steam inhalation + Chyawanprash — daily",
        "headache": "Peppermint oil massage + Shavasana — 10 mins",
        "back pain": "Mahanarayan tailam massage + gentle Bhujangasana",
        "asthma": "Sitopaladi churna — 1 tsp with honey twice daily",
        "diabetes": "Karela juice — morning (empty stomach)",
        "stress": "Ashwagandha — 1 tsp with warm milk at night",
    }
    if request.method == "POST":
        disease = (request.form.get("disease") or "").lower().strip()
        remedy = ayur_map.get(disease, "No standard remedy found. Consult an Ayurvedic doctor.")
        # Increment ayurvedic counter
        session["ayurvedic_count"] = session.get("ayurvedic_count", 0) + 1
    return render_template("ayurvedic.html", disease=disease, remedy=remedy, brand="Health Care")

# ------------------------------ Wellness Dashboard ------------------------------

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    # Initialize session counters if missing
    if "yoga_sessions" not in session:
        session["yoga_sessions"] = 0
    if "allopathic_count" not in session:
        session["allopathic_count"] = 0
    if "ayurvedic_count" not in session:
        session["ayurvedic_count"] = 0

    # Prepare stats
    stats = {
        "yoga_sessions": session.get("yoga_sessions", 0),
        "allopathic_count": session.get("allopathic_count", 0),
        "ayurvedic_count": session.get("ayurvedic_count", 0)
    }

    # Calculate wellness score (average of recent history or default)
    wellness_history = session.get("wellness_history", [])
    if wellness_history:
        wellness_score = sum(h["score"] for h in wellness_history) // len(wellness_history)
    else:
        wellness_score = 75

    # Health tips rotation
    health_tips = [
        "Drink 8 glasses of water daily for optimal hydration.",
        "Practice deep breathing for 5 minutes to reduce stress.",
        "Get 7-8 hours of quality sleep each night.",
        "Include leafy greens in your diet for better nutrition.",
        "Take a 30-minute walk daily to boost your mood and energy."
    ]
    health_tip = health_tips[datetime.now().day % len(health_tips)]

    # Demo consultations
    recent_consultations = [
        {"doctor": "Dr. Sharma", "topic": "General Checkup", "date": "Nov 8"},
        {"doctor": "Dr. Patel", "topic": "Stress Management", "date": "Nov 5"}
    ]

    return render_template(
        "dashboard.html",
        user_email=session["user"],
        stats=stats,
        wellness_score=wellness_score,
        next_appointment="Nov 15",
        health_tip=health_tip,
        recent_consultations=recent_consultations,
        year=datetime.now().year,
        brand="Health Care"
    )

# ------------------------------ Symptom Checker ------------------------------

@app.route("/symptom_checker", methods=["GET", "POST"])
@login_required
def symptom_checker():
    result = None
    selected_symptoms = []
    
    # Symptom database with conditions
    symptom_conditions = {
        "fever": ["Common Cold", "Flu", "COVID-19", "Dengue", "Malaria"],
        "cough": ["Common Cold", "Flu", "COVID-19", "Bronchitis", "Asthma"],
        "headache": ["Migraine", "Tension Headache", "Sinusitis", "Flu", "Dehydration"],
        "fatigue": ["Anemia", "Thyroid Issues", "Diabetes", "Depression", "Sleep Disorder"],
        "body_ache": ["Flu", "Dengue", "Fibromyalgia", "Arthritis"],
        "sore_throat": ["Common Cold", "Flu", "Strep Throat", "Tonsillitis"],
        "runny_nose": ["Common Cold", "Allergies", "Sinusitis"],
        "shortness_breath": ["Asthma", "COVID-19", "Anxiety", "Heart Issues"],
        "nausea": ["Food Poisoning", "Gastritis", "Migraine", "Pregnancy"],
        "dizziness": ["Low Blood Pressure", "Dehydration", "Anemia", "Inner Ear Issues"],
        "chest_pain": ["Heart Issues", "Anxiety", "Acid Reflux", "Muscle Strain"],
        "stomach_pain": ["Gastritis", "Food Poisoning", "IBS", "Appendicitis"],
        "diarrhea": ["Food Poisoning", "IBS", "Gastroenteritis"],
        "constipation": ["IBS", "Dehydration", "Poor Diet"],
        "rash": ["Allergies", "Eczema", "Fungal Infection", "Viral Infection"],
        "joint_pain": ["Arthritis", "Gout", "Injury", "Lupus"],
        "back_pain": ["Muscle Strain", "Poor Posture", "Herniated Disc", "Kidney Issues"],
        "insomnia": ["Stress", "Anxiety", "Depression", "Sleep Disorder"]
    }
    
    if request.method == "POST":
        selected_symptoms = request.form.getlist("symptoms")
        
        if selected_symptoms:
            # Count condition occurrences
            condition_scores = {}
            for symptom in selected_symptoms:
                conditions = symptom_conditions.get(symptom, [])
                for condition in conditions:
                    condition_scores[condition] = condition_scores.get(condition, 0) + 1
            
            # Sort by frequency
            sorted_conditions = sorted(condition_scores.items(), key=lambda x: x[1], reverse=True)
            top_conditions = sorted_conditions[:5]
            
            # Determine urgency
            urgent_symptoms = {"chest_pain", "shortness_breath", "severe_headache"}
            is_urgent = any(s in urgent_symptoms for s in selected_symptoms)
            
            # Get specialist recommendation
            specialist_map = {
                "Common Cold": "General Physician",
                "Flu": "General Physician",
                "COVID-19": "General Physician / Infectious Disease",
                "Asthma": "Pulmonologist",
                "Migraine": "Neurologist",
                "Heart Issues": "Cardiologist",
                "Diabetes": "Endocrinologist",
                "Arthritis": "Rheumatologist",
                "Gastritis": "Gastroenterologist",
                "Depression": "Psychiatrist",
                "Anxiety": "Psychiatrist / Psychologist",
                "Allergies": "Allergist",
                "Skin Issues": "Dermatologist"
            }
            
            # Home care tips
            home_care = []
            if "fever" in selected_symptoms:
                home_care.append("Rest and stay hydrated. Take paracetamol if needed.")
            if "cough" in selected_symptoms:
                home_care.append("Drink warm water with honey. Steam inhalation helps.")
            if "headache" in selected_symptoms:
                home_care.append("Rest in a dark room. Apply cold compress on forehead.")
            if "fatigue" in selected_symptoms:
                home_care.append("Get adequate sleep (7-8 hours). Eat nutritious meals.")
            if "stomach_pain" in selected_symptoms:
                home_care.append("Eat light, bland foods. Avoid spicy and oily food.")
            
            if not home_care:
                home_care.append("Rest well and monitor your symptoms.")
            
            specialist = "General Physician"
            if top_conditions:
                specialist = specialist_map.get(top_conditions[0][0], "General Physician")
            
            result = {
                "possible_conditions": [c[0] for c in top_conditions],
                "match_count": [c[1] for c in top_conditions],
                "is_urgent": is_urgent,
                "specialist": specialist,
                "home_care": home_care,
                "symptom_count": len(selected_symptoms)
            }
    
    return render_template(
        "symptom_checker.html",
        result=result,
        selected_symptoms=selected_symptoms,
        brand="Health Care"
    )

# ------------------------------ BMI / Fitness Lab ------------------------------

@app.route("/bmi", methods=["GET", "POST"])
@login_required
def bmi():
    result, error = None, ""

    defaults = {
        "height_cm": "",
        "weight_kg": "",
        "waist_cm": "",
        "age": "",
        "sex": "male",
        "activity": "moderate"
    }

    if request.method == "POST":
        try:
            height_cm = float(request.form.get("height_cm") or 0)
            weight_kg = float(request.form.get("weight_kg") or 0)
            waist_cm  = float(request.form.get("waist_cm")  or 0)
            age       = int(float(request.form.get("age")   or 0))
        except:
            height_cm, weight_kg, waist_cm, age = 0, 0, 0, 0

        sex       = (request.form.get("sex") or "male").lower()
        activity  = (request.form.get("activity") or "moderate").lower()

        defaults.update({
            "height_cm": height_cm or "",
            "weight_kg": weight_kg or "",
            "waist_cm": waist_cm or "",
            "age": age or "",
            "sex": sex,
            "activity": activity
        })

        if height_cm <= 0 or weight_kg <= 0 or age <= 0:
            error = "Please enter valid height, weight and age."
        elif sex not in ("male", "female"):
            error = "Invalid sex selected."
        else:
            h_m = height_cm / 100.0
            bmi_val = weight_kg / (h_m * h_m)

            if bmi_val < 18.5:
                bmi_cat = "Underweight"
            elif bmi_val < 25:
                bmi_cat = "Normal"
            elif bmi_val < 30:
                bmi_cat = "Overweight"
            else:
                bmi_cat = "Obesity"

            whtr = round((waist_cm / height_cm), 2) if waist_cm > 0 else None
            whtr_cat = None
            if whtr is not None:
                if whtr < 0.4:
                    whtr_cat = "Low (possible under-fat)"
                elif whtr < 0.5:
                    whtr_cat = "Healthy"
                elif whtr < 0.6:
                    whtr_cat = "Increased risk"
                else:
                    whtr_cat = "High risk"

            # BMR (Mifflin–St Jeor)
            if sex == "male":
                bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
            else:
                bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

            factors = {
                "sedentary": 1.2,
                "light": 1.375,
                "moderate": 1.55,
                "active": 1.725,
                "veryactive": 1.9
            }
            tdee = bmr * factors.get(activity, 1.55)

            yoga_suggestions = {
                "Underweight": ["Surya Namaskar", "Bridge Pose", "Bhujangasana"],
                "Normal": ["Vajrasana", "Cat-Cow Pose", "Warrior Pose"],
                "Overweight": ["Tadasana", "Balasana", "Anulom Vilom"],
                "Obesity": ["Utkatasana (gentle)", "Viparita Karani", "Nadi Shodhana"]
            }
            tips = {
                "Underweight": "Add calorie-dense nutritious foods (nuts, dairy, legumes). 3 meals + 2 snacks.",
                "Normal": "Great balance! Maintain with regular yoga, protein, and 7–8h sleep.",
                "Overweight": "Prioritize protein & veggies, portion control, daily walks + yoga.",
                "Obesity": "Start low-impact movement; track intake; consider doctor guidance."
            }

            result = {
                "bmi": round(bmi_val, 1),
                "bmi_cat": bmi_cat,
                "whtr": whtr,
                "whtr_cat": whtr_cat,
                "bmr": int(round(bmr)),
                "tdee": int(round(tdee)),
                "poses": yoga_suggestions[bmi_cat],
                "tip": tips[bmi_cat],
                "activity": activity
            }

    return render_template("bmi.html", result=result, error=error, defaults=defaults, brand="Health Care")

# -------------------- FEEDBACK (simple stub) --------------------
@app.route("/feedback", methods=["GET", "POST"])
@login_required
def feedback():
    msg = None
    if request.method == "POST":
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        message = request.form.get("message", "")
        # (You can save to DB later if you want)
        msg = "Thanks for your feedback!"
    return render_template("feedback.html", msg=msg, brand="Health Care")

# ------------------------------------ API Endpoints ------------------------------------

@app.route('/api/save_appointment', methods=['POST'])
def save_appointment():
    """
    Receives appointment data from Make.com automation
    and saves it to the database.
    """
    try:
        logger.info("Received appointment save request")
        
        # Get JSON data
        if not request.is_json:
            logger.error("Request is not JSON")
            return jsonify({
                "status": "error",
                "message": "Content-Type must be application/json"
            }), 400
            
        data = request.get_json()
        logger.info(f"Received data: {data}")
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'doctor_type', 'issue', 'appointment_date', 'appointment_time']
        missing_fields = []
        
        for field in required_fields:
            if field not in data or not str(data[field]).strip():
                missing_fields.append(field)
        
        if missing_fields:
            logger.error(f"Missing fields: {missing_fields}")
            return jsonify({
                "status": "error",
                "message": f"Missing required fields: {', '.join(missing_fields)}",
                "missing_fields": missing_fields
            }), 400

        # Validate email format
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, data['email']):
            logger.error(f"Invalid email format: {data['email']}")
            return jsonify({
                "status": "error",
                "message": "Invalid email format"
            }), 400

        # Parse and validate date
        try:
            # Try multiple date formats
            date_formats = ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d']
            appointment_date = None
            
            for fmt in date_formats:
                try:
                    appointment_date = datetime.strptime(data['appointment_date'], fmt).date()
                    break
                except ValueError:
                    continue
            
            if not appointment_date:
                raise ValueError("No valid date format found")
                
        except ValueError as e:
            logger.error(f"Invalid date format: {data['appointment_date']}")
            return jsonify({
                "status": "error",
                "message": "Invalid date format. Use YYYY-MM-DD, MM/DD/YYYY, or DD/MM/YYYY"
            }), 400

        # Validate time format
        time_pattern = r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9](\s?(AM|PM))?$'
        if not re.match(time_pattern, data['appointment_time'], re.IGNORECASE):
            logger.error(f"Invalid time format: {data['appointment_time']}")
            return jsonify({
                "status": "error",
                "message": "Invalid time format. Use HH:MM or HH:MM AM/PM"
            }), 400

        # Check for duplicate appointments
        existing_appointment = Appointment.query.filter_by(
            patient_email=data['email'],
            appointment_date=appointment_date,
            appointment_time=data['appointment_time']
        ).first()
        
        if existing_appointment:
            logger.warning(f"Duplicate appointment attempt: {data['email']} on {appointment_date}")
            return jsonify({
                "status": "error",
                "message": "An appointment already exists for this email, date, and time"
            }), 409

        # Create new appointment record
        new_appointment = Appointment(
            patient_name=data['name'].strip(),
            patient_email=data['email'].strip().lower(),
            patient_phone=data['phone'].strip(),
            doctor_type=data.get('doctor_type', 'General Physician').strip(),
            health_issue=data.get('issue', '').strip(),
            appointment_date=appointment_date,
            appointment_time=data['appointment_time'].strip(),
            status='confirmed',
            created_at=datetime.utcnow()
        )

        db.session.add(new_appointment)
        db.session.commit()
        
        logger.info(f"Appointment saved successfully: ID {new_appointment.id}")

        return jsonify({
            "status": "success",
            "message": "Appointment saved successfully",
            "appointment_id": new_appointment.id,
            "appointment": new_appointment.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Database error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Internal server error: {str(e)}"
        }), 500

@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    """Get all appointments (for admin view)"""
    try:
        appointments = Appointment.query.order_by(Appointment.appointment_date.desc()).all()
        logger.info(f"Retrieved {len(appointments)} appointments")
        return jsonify({
            "status": "success",
            "count": len(appointments),
            "appointments": [apt.to_dict() for apt in appointments]
        }), 200
    except Exception as e:
        logger.error(f"Error retrieving appointments: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Test database connection
        from sqlalchemy import text
        db.session.execute(text('SELECT 1'))
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "database": "connected"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }), 500

# ------------------------------------ Run --------------------------------------

if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)   