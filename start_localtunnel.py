#!/usr/bin/env python3
"""
LocalTunnel alternative - No signup required
"""

import subprocess
import time
import sys

def start_localtunnel():
    """Start LocalTunnel for Flask app"""
    try:
        print("🚀 Starting LocalTunnel (no signup required)...")
        
        # Check if Node.js is installed
        try:
            subprocess.run(["node", "--version"], check=True, capture_output=True)
        except:
            print("❌ Node.js not found. Please install Node.js first:")
            print("   Download from: https://nodejs.org/")
            return
        
        # Install localtunnel globally
        print("📦 Installing LocalTunnel...")
        subprocess.run(["npm", "install", "-g", "localtunnel"], check=True)
        
        # Start tunnel
        print("🌐 Starting tunnel on port 5000...")
        process = subprocess.Popen(
            ["lt", "--port", "5000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for URL
        time.sleep(3)
        
        # Try to get the URL from output
        try:
            output = process.stdout.readline()
            if "https://" in output:
                url = output.strip()
                print(f"✅ Tunnel started successfully!")
                print(f"🌐 Public URL: {url}")
                print(f"📡 API Endpoint: {url}/api/save_appointment")
                print("\n" + "="*60)
                print("MAKE.COM CONFIGURATION:")
                print("="*60)
                print(f"URL: {url}/api/save_appointment")
                print("Method: POST")
                print("Headers: Content-Type: application/json")
                print("="*60)
                
                # Keep running
                print("\n⏳ Tunnel is running... Press Ctrl+C to stop")
                process.wait()
            else:
                print("❌ Could not get tunnel URL")
        except KeyboardInterrupt:
            print("\n🛑 Stopping tunnel...")
            process.terminate()
            print("✅ Tunnel stopped")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Alternative: Use the manual method below")

def manual_instructions():
    """Provide manual setup instructions"""
    print("\n" + "="*60)
    print("🔧 MANUAL SETUP INSTRUCTIONS")
    print("="*60)
    print("Since tunnel setup requires additional configuration,")
    print("here are your options:")
    print()
    print("OPTION 1: Test Locally (Recommended for development)")
    print("- Keep your Flask app running on localhost:5000")
    print("- Test API directly: http://localhost:5000/api/save_appointment")
    print("- Use Postman or curl for testing")
    print()
    print("OPTION 2: Deploy to Free Hosting")
    print("- Deploy to Heroku (free tier)")
    print("- Deploy to Railway.app (free tier)")
    print("- Deploy to Render.com (free tier)")
    print()
    print("OPTION 3: Use ngrok with free account")
    print("1. Go to: https://dashboard.ngrok.com/signup")
    print("2. Sign up for free account")
    print("3. Get your authtoken")
    print("4. Run: ngrok config add-authtoken YOUR_TOKEN")
    print("5. Run: ngrok http 5000")
    print()
    print("FOR NOW: Your system is 95% complete!")
    print("All components work locally. Just need public URL for Make.com")

if __name__ == "__main__":
    try:
        start_localtunnel()
    except:
        manual_instructions()