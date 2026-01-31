#!/usr/bin/env python3
"""
Simple Database Initialization Script
Creates all tables with the simplified schema and adds sample data
"""

from app import app, db
from models import User, Appointment
from datetime import datetime, timedelta
import os

def init_database():
    """Initialize database with simplified schema"""
    with app.app_context():
        # Try to remove existing database files if they exist
        db_files = ['healthcare.db', 'instance/healthcare.db', 'instance/users.db']
        for db_file in db_files:
            if os.path.exists(db_file):
                try:
                    os.remove(db_file)
                    print(f"Removed existing database: {db_file}")
                except PermissionError:
                    print(f"Warning: Could not remove {db_file} (file in use). Will recreate tables instead.")
        
        # Create all tables (this will create new tables or update existing ones)
        db.create_all()
        print("Created all database tables with simplified schema")
        
        # Create sample users
        admin_user = User(email='admin@healthcare.com')
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        
        regular_user = User(email='user@healthcare.com')
        regular_user.set_password('user123')
        db.session.add(regular_user)
        
        test_user = User(email='test@test.com')
        test_user.set_password('test123')
        db.session.add(test_user)
        
        # Commit users
        db.session.commit()
        
        # Create sample appointment
        sample_appointment = Appointment(
            patient_name='John Doe',
            patient_email='user@healthcare.com',
            patient_phone='+1234567890',
            doctor_type='General Physician',
            health_issue='Regular checkup',
            appointment_date=datetime.now().date() + timedelta(days=7),
            appointment_time='10:00 AM',
            status='confirmed'
        )
        db.session.add(sample_appointment)
        
        # Commit all changes
        db.session.commit()
        
        print("Sample data created successfully!")
        print("\nSample Login Credentials:")
        print("Admin: admin@healthcare.com / admin123")
        print("User: user@healthcare.com / user123")
        print("Test: test@test.com / test123")
        
        return True

if __name__ == "__main__":
    print("Initializing Simple Healthcare Database...")
    success = init_database()
    if success:
        print("\nDatabase initialization completed successfully!")
        print("You can now run the application with: python app.py")
    else:
        print("Database initialization failed!")