from flask import Flask, render_template, request, redirect, url_for, session
from yoga_suggestions import suggest_yoga
import os, random, time
from datetime import datetime

app = Flask(__name__)
app.secret_key = "healthcare_secret"

# ---------------- In-memory demo stores (reset on server restart) ----------------
users = {}           # {email: password}
reset_tokens = {}    # {email: {"code": "123456", "expires": <epoch>}}

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
            elif email in users:
                msg = "User already exists!"
            else:
                users[email] = password
                msg = "Registered successfully! Please log in."
        elif action == "login":
            if email in users and users[email] == password:
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
        elif email_entered not in users:
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
            elif email not in users:
                msg = "Account not found."
            else:
                users[email] = new_pwd
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

@app.route("/consult", methods=["GET", "POST"])
def consult():
    if "user" not in session:
        return redirect(url_for("login_register"))

    confirmation = None
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        disease = (request.form.get("disease") or "").strip()
        doctor_type = (request.form.get("doctor_type") or "").strip()
        description = (request.form.get("description") or "").strip()
        confirmation = {
            "name": name or "Not provided",
            "disease": disease or "Not provided",
            "doctor_type": doctor_type or "Not provided",
            "description": description or "—"
        }
    return render_template("consult.html", confirmation=confirmation, brand="Health Care")

@app.route("/yoga", methods=["GET", "POST"])
def yoga():
    poses = []
    disease = ""
    if request.method == "POST":
        disease = (request.form.get("disease") or "").strip()
        if disease:
            poses = suggest_yoga(disease)
    return render_template("yoga.html", poses=poses, disease=disease, brand="Health Care")

@app.route("/allopathic", methods=["GET", "POST"])
def allopathic():
    suggestion = None
    disease = ""
    allopathy_map = {
        "fever": "Paracetamol 500 mg — 1 tablet every 8 hours after food",
        "cold": "Cetirizine 10 mg — once at night",
        "headache": "Paracetamol 500 mg — as needed after food",
        "back pain": "Ibuprofen 400 mg — twice daily + local heat",
        "asthma": "Salbutamol inhaler — 2 puffs as needed",
        "diabetes": "Metformin 500 mg — morning & night with food",
        "stress": "Vitamin B-complex — once daily",
    }
    if request.method == "POST":
        disease = (request.form.get("disease") or "").lower().strip()
        suggestion = allopathy_map.get(disease, "No ready suggestion found. Please consult a doctor.")
    return render_template("allopathic.html", disease=disease, suggestion=suggestion, brand="Health Care")

@app.route("/ayurvedic", methods=["GET", "POST"])
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
    return render_template("ayurvedic.html", disease=disease, remedy=remedy, brand="Health Care")

# ------------------------------ Wellness Dashboard ------------------------------

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("login_register"))

    # init demo 7-day history if missing
    if "wellness_history" not in session:
        session["wellness_history"] = [
            {"label": f"D{i}", "score": random.randint(58, 82)} for i in range(1, 7)
        ] + [{"label": "Today", "score": random.randint(60, 85)}]

    result = None
    today_inputs = {"mood": "ok", "sleep": 7, "stress": 4}

    if request.method == "POST":
        mood = (request.form.get("mood") or "ok").strip().lower()
        sleep = request.form.get("sleep") or "7"
        stress = request.form.get("stress") or "4"

        score, condition, yoga_list, ayur, allo = compute_insights(mood, sleep, stress)
        result = {"score": score, "condition": condition, "yoga": yoga_list, "ayur": ayur, "allo": allo}
        today_inputs = {"mood": mood, "sleep": int(sleep), "stress": int(stress)}

        # update history → keep last 7
        hist = session.get("wellness_history", [])
        hist.append({"label": "Today", "score": score})
        session["wellness_history"] = hist[-7:]

    chart_scores = [row["score"] for row in session.get("wellness_history", [])]
    chart_labels = [row["label"] for row in session.get("wellness_history", [])]
    if chart_labels:
        chart_labels[-1] = "Today"

    return render_template(
        "dashboard.html",
        user=session["user"],
        result=result,
        today_inputs=today_inputs,
        chart_labels=chart_labels,
        chart_scores=chart_scores,
        brand="Health Care"
    )

# ------------------------------ BMI / Fitness Lab ------------------------------
# -------------------- FEEDBACK (simple stub) --------------------
@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    msg = None
    if request.method == "POST":
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        message = request.form.get("message", "")
        # (You can save to DB later if you want)
        msg = "Thanks for your feedback!"
    return render_template("feedback.html", msg=msg)


@app.route("/bmi", methods=["GET", "POST"])
def bmi():
    if "user" not in session:
        return redirect(url_for("login_register"))

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
                "Normal": ["Vajrasana", "Cat-Cow Pose", "Shavasana"],
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

# ------------------------------------ Run --------------------------------------

if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
