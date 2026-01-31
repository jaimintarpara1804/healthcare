from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta
import json

db = SQLAlchemy()

# ---------- Simple User Model ----------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# ---------- Simple Appointment System ----------
class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    patient_email = db.Column(db.String(120), nullable=False)
    patient_phone = db.Column(db.String(20))
    doctor_type = db.Column(db.String(50), nullable=False)
    health_issue = db.Column(db.Text)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed, cancelled
    consultation_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Appointment {self.patient_name} - {self.appointment_date}>'

    def to_dict(self):
        return {
            'id': self.id,
            'patient_name': self.patient_name,
            'patient_email': self.patient_email,
            'patient_phone': self.patient_phone,
            'doctor_type': self.doctor_type,
            'health_issue': self.health_issue,
            'appointment_date': self.appointment_date.strftime('%Y-%m-%d') if self.appointment_date else None,
            'appointment_time': self.appointment_time,
            'status': self.status,
            'consultation_notes': self.consultation_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# ---------- Optional: store consultation requests ----------
class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    issue = db.Column(db.String(200))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
