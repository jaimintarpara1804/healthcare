#!/usr/bin/env python3
"""
Database Migration Script
Adds missing columns to existing database
"""

import sqlite3
import os
from datetime import datetime

def migrate_database():
    """Add missing columns to existing database"""
    
    # Database paths to check
    db_paths = ['healthcare.db', 'instance/healthcare.db', 'instance/users.db']
    
    for db_path in db_paths:
        if os.path.exists(db_path):
            print(f"Migrating database: {db_path}")
            
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Check if user table exists
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user';")
                if cursor.fetchone():
                    print("Found user table, checking columns...")
                    
                    # Get existing columns
                    cursor.execute("PRAGMA table_info(user);")
                    existing_columns = [row[1] for row in cursor.fetchall()]
                    print(f"Existing columns: {existing_columns}")
                    
                    # Add missing columns
                    new_columns = [
                        ("first_name", "VARCHAR(50)", "''"),
                        ("last_name", "VARCHAR(50)", "''"),
                        ("phone", "VARCHAR(20)", "NULL"),
                        ("date_of_birth", "DATE", "NULL"),
                        ("gender", "VARCHAR(10)", "NULL"),
                        ("role", "VARCHAR(10)", "'user'"),
                        ("is_active", "BOOLEAN", "1"),
                        ("email_verified", "BOOLEAN", "0"),
                        ("phone_verified", "BOOLEAN", "0"),
                        ("created_at", "DATETIME", f"'{datetime.utcnow()}'"),
                        ("updated_at", "DATETIME", f"'{datetime.utcnow()}'"),
                        ("last_login", "DATETIME", "NULL")
                    ]
                    
                    for column_name, column_type, default_value in new_columns:
                        if column_name not in existing_columns:
                            try:
                                cursor.execute(f"ALTER TABLE user ADD COLUMN {column_name} {column_type} DEFAULT {default_value};")
                                print(f"Added column: {column_name}")
                            except sqlite3.OperationalError as e:
                                if "duplicate column name" not in str(e):
                                    print(f"Error adding column {column_name}: {e}")
                    
                    # Update existing users with default names if they don't have them
                    cursor.execute("UPDATE user SET first_name = 'User', last_name = 'Name' WHERE first_name IS NULL OR first_name = '';")
                    cursor.execute("UPDATE user SET role = 'user' WHERE role IS NULL OR role = '';")
                    
                    conn.commit()
                    print("Migration completed successfully!")
                
                conn.close()
                
            except Exception as e:
                print(f"Error migrating {db_path}: {e}")
                continue
    
    return True

if __name__ == "__main__":
    print("Starting database migration...")
    migrate_database()
    print("Migration completed!")