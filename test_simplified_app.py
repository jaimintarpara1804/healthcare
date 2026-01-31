#!/usr/bin/env python3
"""
Test script for simplified healthcare application
Tests core functionality after removing subscription features
"""

import sys
import os

def test_imports():
    """Test that all modules import correctly"""
    print("Testing imports...")
    try:
        import app
        print("✅ app.py imports successfully")
        
        import models
        print("✅ models.py imports successfully")
        
        import yoga_suggestions
        print("✅ yoga_suggestions.py imports successfully")
        
        import yoga_data
        print("✅ yoga_data.py imports successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_database_models():
    """Test database models"""
    print("\nTesting database models...")
    try:
        from models import User, Appointment, Consultation
        from app import app, db
        
        with app.app_context():
            # Test User model
            user = User(email="test@example.com")
            user.set_password("testpass")
            print("✅ User model works")
            
            # Test password checking
            if user.check_password("testpass"):
                print("✅ Password hashing/checking works")
            else:
                print("❌ Password checking failed")
                return False
            
            # Test Appointment model
            from datetime import date
            appointment = Appointment(
                patient_name="Test Patient",
                patient_email="test@example.com",
                doctor_type="General Physician",
                appointment_date=date.today(),
                appointment_time="10:00 AM"
            )
            print("✅ Appointment model works")
            
        return True
    except Exception as e:
        print(f"❌ Database model error: {e}")
        return False

def test_core_functions():
    """Test core application functions"""
    print("\nTesting core functions...")
    try:
        from app import compute_insights
        
        # Test compute_insights function
        score, condition, yoga_list, ayur_tip, allo_tip = compute_insights("happy", "7", "3")
        
        if isinstance(score, int) and 0 <= score <= 100:
            print("✅ compute_insights function works")
        else:
            print("❌ compute_insights function failed")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Core function error: {e}")
        return False

def test_yoga_suggestions():
    """Test yoga suggestion functionality"""
    print("\nTesting yoga suggestions...")
    try:
        from yoga_suggestions import suggest_yoga
        
        suggestions = suggest_yoga("stress")
        if isinstance(suggestions, list) and len(suggestions) > 0:
            print("✅ Yoga suggestions work")
        else:
            print("❌ Yoga suggestions failed")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Yoga suggestions error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Simplified Healthcare Application")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_database_models,
        test_core_functions,
        test_yoga_suggestions
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        else:
            print(f"❌ Test failed: {test.__name__}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The simplified application is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)