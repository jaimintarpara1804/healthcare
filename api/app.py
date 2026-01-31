from flask import Flask, jsonify, render_template_string
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "healthcare_secret_2024_secure")

# Simple HTML template for testing
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Healthcare App</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .status { padding: 20px; background: #e8f5e8; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Healthcare Application</h1>
        <div class="status">
            <h2>✅ Application Status: Running</h2>
            <p>Your Flask application is successfully deployed on Vercel!</p>
            <p><strong>Environment:</strong> {{ env }}</p>
            <p><strong>Python Path:</strong> {{ python_path }}</p>
        </div>
        
        <h3>Available Endpoints:</h3>
        <ul>
            <li><a href="/health">/health</a> - Health check</li>
            <li><a href="/api/test">/api/test</a> - API test</li>
        </ul>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    import sys
    return render_template_string(HTML_TEMPLATE, 
                                env="Vercel" if os.environ.get('VERCEL') else "Local",
                                python_path=sys.path[:3])

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "message": "Flask app is running on Vercel",
        "environment": "vercel" if os.environ.get('VERCEL') else "local"
    })

@app.route('/api/test')
def api_test():
    return jsonify({
        "message": "API is working!",
        "status": "success",
        "data": {
            "app": "Healthcare System",
            "version": "1.0.0"
        }
    })

if __name__ == "__main__":
    app.run(debug=True)