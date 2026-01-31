#!/usr/bin/env python3
"""
Quick test for Digital Health Twin functionality
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:5000"
TEST_USER_ID = 1

def quick_test():
    """Quick test of key endpoints"""
    
    print("🧪 Quick Digital Health Twin Test")
    print("=" * 40)
    
    # Test health check
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        print(f"✅ Health Check: {response.status_code}")
    except Exception as e:
        print(f"❌ Health Check Failed: {e}")
        return
    
    # Test update health twin
    update_data = {
        "age": 30,
        "gender": "male", 
        "height_cm": 175,
        "weight": 70,
        "stress_level": 5,
        "sleep_quality": 7,
        "activity_level": "moderate"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/health_twin/{TEST_USER_ID}/update",
            json=update_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"✅ Update Health Twin: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Message: {data.get('message', 'Success')}")
    except Exception as e:
        print(f"❌ Update Failed: {e}")
    
    # Test get health twin
    try:
        response = requests.get(f"{BASE_URL}/api/health_twin/{TEST_USER_ID}", timeout=5)
        print(f"✅ Get Health Twin: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            health_twin = data.get('health_twin', {})
            print(f"   Health Score: {health_twin.get('health_score', 'N/A')}")
    except Exception as e:
        print(f"❌ Get Health Twin Failed: {e}")
    
    # Test analytics
    try:
        response = requests.get(f"{BASE_URL}/api/health_twin/{TEST_USER_ID}/analytics?days=30", timeout=10)
        print(f"✅ Analytics: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            analytics = data.get('analytics', {})
            print(f"   Period: {analytics.get('period', 'N/A')}")
    except Exception as e:
        print(f"❌ Analytics Failed: {e}")
    
    # Test goals
    try:
        response = requests.get(f"{BASE_URL}/api/health_twin/{TEST_USER_ID}/goals", timeout=5)
        print(f"✅ Goals: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            goals = data.get('goals', [])
            print(f"   Goals Count: {len(goals)}")
    except Exception as e:
        print(f"❌ Goals Failed: {e}")
    
    print("\n🏁 Quick test complete!")

if __name__ == "__main__":
    quick_test()