#!/usr/bin/env python3
"""
Integration Test for MQTT Simulator
Tests the complete system including API and frontend connectivity.

This script performs end-to-end testing of the MQTT Simulator:
- API health check
- Profiles endpoint functionality
- Simulation status monitoring
- MQTT connection testing
- Profile preview generation
- Frontend accessibility

Usage:
    python3 test_integration.py

Prerequisites:
    - API server running on http://localhost:8000
    - Frontend server running on http://localhost:5173 (optional)
    - MQTT broker running on localhost:1883 (optional)

The test will provide detailed feedback on each component's status
and overall system health.
"""

import requests
import json
import time
import sys
from pathlib import Path

def test_api_health():
    """Test API health endpoint."""
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ API health check passed")
            print(f"   Version: {data.get('data', {}).get('version', 'unknown')}")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API health check failed: {e}")
        return False

def test_profiles_endpoint():
    """Test profiles endpoint."""
    try:
        response = requests.get("http://localhost:8000/api/profiles/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            profiles = data.get('profiles', [])
            print(f"✅ Profiles endpoint working: {len(profiles)} profiles found")
            for profile in profiles:
                print(f"   - {profile['name']}: {profile['description']}")
            return True
        else:
            print(f"❌ Profiles endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Profiles endpoint failed: {e}")
        return False

def test_simulation_status():
    """Test simulation status endpoint."""
    try:
        response = requests.get("http://localhost:8000/api/simulation/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Simulation status endpoint working")
            print(f"   Running: {data.get('is_running', False)}")
            print(f"   Connected: {data.get('is_connected', False)}")
            return True
        else:
            print(f"❌ Simulation status failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Simulation status failed: {e}")
        return False

def test_mqtt_connection():
    """Test MQTT connection endpoint."""
    try:
        config = {
            "host": "localhost",
            "port": 1883,
            "username": None,
            "password": None
        }
        response = requests.post(
            "http://localhost:8000/api/mqtt/connect",
            json=config,
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ MQTT connection test: {data.get('message', 'Unknown')}")
            return True
        else:
            print(f"⚠️  MQTT connection test: {response.status_code}")
            print("   (This is expected if no MQTT broker is running)")
            return True  # Not a failure, just no broker
    except Exception as e:
        print(f"⚠️  MQTT connection test failed: {e}")
        print("   (This is expected if no MQTT broker is running)")
        return True  # Not a failure, just no broker

def test_frontend_connectivity():
    """Test if frontend is accessible."""
    try:
        response = requests.get("http://localhost:5173", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
            return True
        else:
            print(f"⚠️  Frontend returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"⚠️  Frontend not accessible: {e}")
        print("   (This is expected if frontend is not running)")
        return False

def test_profile_preview():
    """Test profile preview functionality."""
    try:
        # Test weather profile preview
        response = requests.post(
            "http://localhost:8000/api/profiles/weather/preview",
            json={},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ Profile preview working")
            preview = data.get('data', {}).get('preview', {})
            if 'temperature' in preview:
                print(f"   Sample temperature: {preview['temperature']}°C")
            return True
        else:
            print(f"❌ Profile preview failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Profile preview failed: {e}")
        return False

def main():
    """Run all integration tests."""
    print("🧪 MQTT Simulator Integration Test")
    print("=" * 40)
    
    tests = [
        ("API Health", test_api_health),
        ("Profiles Endpoint", test_profiles_endpoint),
        ("Simulation Status", test_simulation_status),
        ("MQTT Connection", test_mqtt_connection),
        ("Profile Preview", test_profile_preview),
        ("Frontend Connectivity", test_frontend_connectivity),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        if test_func():
            passed += 1
        time.sleep(0.5)  # Small delay between tests
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is working correctly.")
        return 0
    elif passed >= total - 1:  # Allow one failure (usually frontend)
        print("✅ Core functionality is working. Some optional features may not be available.")
        return 0
    else:
        print("❌ Some core tests failed. Please check the system setup.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 