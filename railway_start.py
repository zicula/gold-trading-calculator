# Railway Start Script (Python version)
import os
import subprocess
import sys

def main():
    # Get port from Railway or default to 8080
    port = os.environ.get('PORT', '8080')
    
    print(f"🚀 Starting Gold Trading Calculator on port {port}")
    print(f"📱 Flask Environment: {os.environ.get('FLASK_ENV', 'development')}")
    print(f"🔧 MT5 Mode: {os.environ.get('MT5_MODE', 'production')}")
    print(f"🐍 Python Path: {os.environ.get('PYTHONPATH', '/app')}")
    
    # Validate port
    try:
        port_int = int(port)
        if port_int < 1 or port_int > 65535:
            raise ValueError("Port must be between 1-65535")
    except ValueError as e:
        print(f"❌ Invalid port '{port}': {e}")
        print("📌 Using default port 8080")
        port = "8080"
    
    # Build gunicorn command
    cmd = [
        'gunicorn',
        '--bind', f'0.0.0.0:{port}',
        '--workers', '1',
        '--timeout', '120',
        '--access-logfile', '-',
        '--error-logfile', '-',
        '--preload',
        'backend.app:app'
    ]
    
    print(f"🔄 Executing: {' '.join(cmd)}")
    
    # Execute gunicorn
    try:
        subprocess.execvp('gunicorn', cmd)
    except Exception as e:
        print(f"❌ Failed to start gunicorn: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
