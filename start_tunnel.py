#!/usr/bin/env python3
"""
Simple tunnel starter for exposing Flask app to Make.com
Uses pyngrok for easy tunnel management
"""

import os
import time
from pyngrok import ngrok

def start_tunnel():
    """Start ngrok tunnel for Flask app"""
    try:
        print("🚀 Starting ngrok tunnel...")
        
        # Kill any existing tunnels
        ngrok.kill()
        
        # Start tunnel on port 5000
        public_tunnel = ngrok.connect(5000)
        public_url = public_tunnel.public_url
        
        print(f"✅ Tunnel started successfully!")
        print(f"🌐 Public URL: {public_url}")
        print(f"📡 API Endpoint: {public_url}/api/save_appointment")
        print(f"🔗 Use this URL in Make.com HTTP module")
        print("\n" + "="*60)
        print("MAKE.COM CONFIGURATION:")
        print("="*60)
        print(f"URL: {public_url}/api/save_appointment")
        print("Method: POST")
        print("Headers: Content-Type: application/json")
        print("="*60)
        
        # Keep tunnel alive
        print("\n⏳ Tunnel is running... Press Ctrl+C to stop")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping tunnel...")
            ngrok.kill()
            print("✅ Tunnel stopped")
            
    except Exception as e:
        print(f"❌ Error starting tunnel: {e}")
        print("💡 Try installing pyngrok: pip install pyngrok")

if __name__ == "__main__":
    start_tunnel()