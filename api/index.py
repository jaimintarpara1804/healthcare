import os
import sys

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import Flask and create a simple app for testing
from flask import Flask

# Try to import the main app, fallback to simple app if it fails
try:
    from app import app
except ImportError as e:
    print(f"Failed to import main app: {e}")
    # Create a minimal Flask app for debugging
    app = Flask(__name__)
    
    @app.route('/')
    def hello():
        return f"Hello from Vercel! Import error: {str(e)}"
    
    @app.route('/health')
    def health():
        return {"status": "ok", "message": "Simple Flask app running"}

# Make sure the app is available for Vercel
application = app

if __name__ == "__main__":
    app.run(debug=True)