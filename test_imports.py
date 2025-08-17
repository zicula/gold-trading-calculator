#!/usr/bin/env python3
"""
Simple test script for Railway deployment debugging
"""

print("=== Testing Python imports ===")

try:
    import sys
    print(f"✅ Python version: {sys.version}")
except Exception as e:
    print(f"❌ Python import failed: {e}")

try:
    import os
    print(f"✅ OS module imported")
    print(f"   PORT env: {os.environ.get('PORT', 'Not set')}")
    print(f"   PYTHON_PATH: {os.environ.get('PYTHONPATH', 'Not set')}")
except Exception as e:
    print(f"❌ OS import failed: {e}")

try:
    import flask
    print(f"✅ Flask version: {flask.__version__}")
except Exception as e:
    print(f"❌ Flask import failed: {e}")

try:
    import jwt
    print(f"✅ JWT imported successfully")
    print(f"   JWT module: {jwt}")
    print(f"   JWT file: {jwt.__file__}")
except Exception as e:
    print(f"❌ JWT import failed: {e}")

try:
    import bcrypt
    print(f"✅ bcrypt imported successfully")
except Exception as e:
    print(f"❌ bcrypt import failed: {e}")

try:
    from flask_cors import CORS
    print(f"✅ flask-cors imported successfully")
except Exception as e:
    print(f"❌ flask-cors import failed: {e}")

# Test JWT functionality
try:
    import jwt
    test_payload = {'test': 'data'}
    test_secret = 'test_secret'
    token = jwt.encode(test_payload, test_secret, algorithm='HS256')
    decoded = jwt.decode(token, test_secret, algorithms=['HS256'])
    print(f"✅ JWT encode/decode test passed")
    print(f"   Token: {token[:50]}...")
    print(f"   Decoded: {decoded}")
except Exception as e:
    print(f"❌ JWT functionality test failed: {e}")

print("=== Import test completed ===")

# Simple Flask app for testing
if __name__ == "__main__":
    try:
        from flask import Flask
        app = Flask(__name__)
        
        @app.route('/test')
        def test():
            return {"status": "ok", "message": "Railway test successful"}
        
        @app.route('/api/status')
        def status():
            return {"status": "healthy", "imports": "all_good"}
        
        port = int(os.environ.get('PORT', 5000))
        print(f"\n🚀 Starting test server on port {port}")
        app.run(host='0.0.0.0', port=port, debug=False)
        
    except Exception as e:
        print(f"❌ Flask app failed: {e}")
        import traceback
        traceback.print_exc()
