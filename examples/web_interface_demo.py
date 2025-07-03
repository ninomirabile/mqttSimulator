#!/usr/bin/env python3
"""
Web Interface Demo
Demonstrates how to use the MQTT Simulator web interface.

This script:
1. Starts a local MQTT broker (if available)
2. Provides instructions for using the web interface
3. Shows example configurations
"""

import subprocess
import sys
import time
import requests
from pathlib import Path

def check_mqtt_broker():
    """Check if a local MQTT broker is running."""
    try:
        import paho.mqtt.client as mqtt
        
        client = mqtt.Client()
        client.connect("localhost", 1883, 5)
        client.disconnect()
        return True
    except:
        return False

def start_mosquitto():
    """Try to start Mosquitto MQTT broker."""
    try:
        # Try to start mosquitto
        process = subprocess.Popen(
            ["mosquitto", "-p", "1883"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(2)  # Give it time to start
        
        if process.poll() is None:
            print("✅ Mosquitto MQTT broker started on port 1883")
            return process
        else:
            print("❌ Failed to start Mosquitto")
            return None
    except FileNotFoundError:
        print("❌ Mosquitto not found. Please install it:")
        print("   Ubuntu/Debian: sudo apt install mosquitto")
        print("   macOS: brew install mosquitto")
        print("   Windows: Download from https://mosquitto.org/download/")
        return None

def check_api():
    """Check if the API is running."""
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    print("🚀 MQTT Simulator Web Interface Demo")
    print("=" * 50)
    
    # Check MQTT broker
    print("\n1. Checking MQTT broker...")
    if check_mqtt_broker():
        print("✅ MQTT broker is running on localhost:1883")
        mosquitto_process = None
    else:
        print("⚠️  No MQTT broker found. Attempting to start Mosquitto...")
        mosquitto_process = start_mosquitto()
        if not mosquitto_process:
            print("❌ Please start an MQTT broker manually or install Mosquitto")
            print("   You can use any MQTT broker (HiveMQ, AWS IoT, etc.)")
    
    # Check API
    print("\n2. Checking API...")
    if check_api():
        print("✅ API is running on http://localhost:8000")
    else:
        print("❌ API is not running. Please start it with:")
        print("   python3 -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000")
        return
    
    # Instructions
    print("\n3. Web Interface Instructions")
    print("=" * 30)
    print("📱 Open your browser and go to: http://localhost:5173")
    print("\n🔧 Configuration Steps:")
    print("   1. Select a profile (weather, agriculture, energy)")
    print("   2. Configure MQTT settings:")
    print("      - Host: localhost")
    print("      - Port: 1883")
    print("      - Username/Password: (leave empty for local broker)")
    print("   3. Click 'Test Connection' to verify MQTT connectivity")
    print("   4. Set simulation interval (e.g., 5 seconds)")
    print("   5. Click 'Start Simulation'")
    print("\n📊 Monitor the simulation:")
    print("   - Watch real-time data in the 'Live Data Stream' section")
    print("   - Check connection and simulation status")
    print("   - View message count and duration")
    
    # Example configurations
    print("\n4. Example Configurations")
    print("=" * 30)
    
    print("\n🌤️  Weather Profile:")
    print("   - Profile: weather")
    print("   - Topic: weather/milano")
    print("   - Data: temperature, humidity, wind_speed, description")
    
    print("\n🌱 Agriculture Profile:")
    print("   - Profile: agriculture")
    print("   - Topic: agriculture/soil/soil-001")
    print("   - Data: moisture, temperature, ph_level")
    
    print("\n⚡ Energy Profile:")
    print("   - Profile: energy")
    print("   - Topic: energy/meter/energy-01")
    print("   - Data: power_kw, voltage_v, current_a, frequency_hz")
    
    # Testing with curl
    print("\n5. API Testing Examples")
    print("=" * 30)
    print("Test the API directly with curl:")
    print("   # Get available profiles")
    print("   curl http://localhost:8000/api/profiles/")
    print("\n   # Get simulation status")
    print("   curl http://localhost:8000/api/simulation/status")
    print("\n   # Test MQTT connection")
    print("   curl -X POST http://localhost:8000/api/mqtt/connect \\")
    print("        -H 'Content-Type: application/json' \\")
    print("        -d '{\"host\":\"localhost\",\"port\":1883}'")
    
    # Troubleshooting
    print("\n6. Troubleshooting")
    print("=" * 20)
    print("❓ Common Issues:")
    print("   - MQTT connection fails: Check if broker is running")
    print("   - API not responding: Restart with uvicorn")
    print("   - Frontend not loading: Check if npm run dev is running")
    print("   - CORS errors: API should allow all origins in development")
    
    print("\n🔧 Useful Commands:")
    print("   # Start API")
    print("   python3 -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000")
    print("\n   # Start Frontend")
    print("   cd frontend && npm run dev")
    print("\n   # Install Mosquitto (Ubuntu/Debian)")
    print("   sudo apt install mosquitto mosquitto-clients")
    
    print("\n🎉 Demo complete! Enjoy using the MQTT Simulator!")
    
    # Keep running if we started mosquitto
    if mosquitto_process:
        try:
            print("\n⏳ Press Ctrl+C to stop the MQTT broker...")
            mosquitto_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping MQTT broker...")
            mosquitto_process.terminate()
            mosquitto_process.wait()

if __name__ == "__main__":
    main() 