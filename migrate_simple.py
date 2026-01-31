#!/usr/bin/env python3
"""
Simple Database Migration Script
Handles schema changes for the simplified healthcare system
"""

import sqlite3
import os
from datetime import datetime

def migrate_database():
    """Migrate existing database to simplified schema"""
    db_path = os.path.join('instance', 'users.db')
    
    if not os.path.exists(db_path):
        print("No existing database found. Run init_database.py instead.")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("Starting database migration...")
        
        # Check if created_at column exists in user table
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'created_at' not in columns:
            print("Adding created_at column to user table...")
            cursor.execute("ALTER TABLE user ADD COLUMN created_at DATETIME")
            # Update existing records with current timestamp
            current_time = datetime.now().isoformat()
            cursor.execute("UPDATE user SET created_at = ? WHERE created_at IS NULL", (current_time,))
        
        # Remove subscription-related tables if they exist
        tables_to_remove = [
            'subscription', 'doctor', 'doctor_patient_assignment', 
            'health_twin', 'health_record', 'notification'
        ]
        
        for table in tables_to_remove:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table}")
                print(f"Removed table: {table}")
            except sqlite3.Error as e:
                print(f"Note: Could not remove table {table}: {e}")
        
        # Ensure appointments table has correct structure
        cursor.execute("PRAGMA table_info(appointments)")
        appointment_columns = [column[1] for column in cursor.fetchall()]
        
        # Remove subscription-related columns from appointments if they exist
        subscription_columns = ['patient_id', 'appointment_type', 'prescription', 'updated_at']
        for col in subscription_columns:
            if col in appointment_columns:
                print(f"Note: Column {col} exists in appointments table but will be ignored")
        
        conn.commit()
        conn.close()
        
        print("Database migration completed successfully!")
        return True
        
    except sqlite3.Error as e:
        print(f"Migration failed: {e}")
        return False

if __name__ == "__main__":
    print("Running Simple Database Migration...")
    success = migrate_database()
    if success:
        print("\nMigration completed! You can now run the application.")
    else:
        print("\nMigration failed! Please check the errors above.")