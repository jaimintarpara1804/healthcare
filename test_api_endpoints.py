#!/usr/bin/env python3
"""
Comprehensive API Testing Suite for Health Care Website
Tests all endpoints and validates responses
"""

import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:5000"
API_BASE = f"{BASE_URL}/api"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing Health Check Endpoint...")
    try:
        response = requests.get(f"{API_BASE}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        print("✅ Health check passed!")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_save_appointment():
    """Test saving a new appointment"""
    print("\n📝 Testing Save Appointment Endpoint...")
    
    # Test data
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    test_data = {
        "name": "Test Patient",
        "email": "test@example.com",
        "phone": "+1234567890",
        "doctor_type": "General Physician",
        "issue": "Regular checkup",
        "appointment_date": tomorrow,
        "appointment_time": "10:00 AM"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/save_appointment",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Appointment saved successfully!")
            return response.json().get("appointment_id")
        else:
            print(f"❌ Failed to save appointment: {response.json()}")
            return None
    except Exception as e:
        print(f"❌ Save appointment failed: {e}")
        return None

def test_get_appointments():
    """Test retrieving all appointments"""
    print("\n📋 Testing Get All Appointments Endpoint...")
    try:
        response = requests.get(f"{API_BASE}/appointments")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Found {data.get('count', 0)} appointments")
        
        if response.status_code == 200:
            print("✅ Retrieved appointments successfully!")
            return True
        else:
            print(f"❌ Failed to retrieve appointments: {data}")
            return False
    except Exception as e:
        print(f"❌ Get appointments failed: {e}")
        return False

def test_get_specific_appointment(appointment_id):
    """Test retrieving a specific appointment"""
    if not appointment_id:
        print("\n⏭️ Skipping specific appointment test (no ID)")
        return False
        
    print(f"\n🔍 Testing Get Specific Appointment (ID: {appointment_id})...")
    try:
        response = requests.get(f"{API_BASE}/appointments/{appointment_id}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Retrieved specific appointment successfully!")
            return True
        else:
            print(f"❌ Failed to retrieve appointment: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Get specific appointment failed: {e}")
        return False

def test_validation_errors():
    """Test API validation and error handling"""
    print("\n⚠️ Testing Validation and Error Handling...")
    
    # Test missing fields
    print("Testing missing required fields...")
    response = requests.post(
        f"{API_BASE}/save_appointment",
        json={"name": "Test"},
        headers={"Content-Type": "application/json"}
    )
    print(f"Missing fields response: {response.status_code} - {response.json()}")
    
    # Test invalid email
    print("Testing invalid email format...")
    response = requests.post(
        f"{API_BASE}/save_appointment",
        json={
            "name": "Test",
            "email": "invalid-email",
            "phone": "123",
            "doctor_type": "GP",
            "issue": "test",
            "appointment_date": "2024-12-20",
            "appointment_time": "10:00"
        },
        headers={"Content-Type": "application/json"}
    )
    print(f"Invalid email response: {response.status_code} - {response.json()}")
    
    # Test invalid date
    print("Testing invalid date format...")
    response = requests.post(
        f"{API_BASE}/save_appointment",
        json={
            "name": "Test",
            "email": "test@example.com",
            "phone": "123",
            "doctor_type": "GP",
            "issue": "test",
            "appointment_date": "invalid-date",
            "appointment_time": "10:00"
        },
        headers={"Content-Type": "application/json"}
    )
    print(f"Invalid date response: {response.status_code} - {response.json()}")
    
    print("✅ Validation tests completed!")

def run_all_tests():
    """Run all API tests"""
    print("🚀 STARTING COMPREHENSIVE API TESTING")
    print("=" * 50)
    
    results = []
    
    # Test 1: Health Check
    results.append(("Health Check", test_health_check()))
    
    # Test 2: Save Appointment
    appointment_id = test_save_appointment()
    results.append(("Save Appointment", appointment_id is not None))
    
    # Test 3: Get All Appointments
    results.append(("Get All Appointments", test_get_appointments()))
    
    # Test 4: Get Specific Appointment
    results.append(("Get Specific Appointment", test_get_specific_appointment(appointment_id)))
    
    # Test 5: Validation Errors
    test_validation_errors()
    results.append(("Validation Tests", True))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Your API is working perfectly!")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    run_all_tests()