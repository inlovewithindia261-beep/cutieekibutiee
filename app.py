from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime
import socket

app = Flask(__name__)

logs = []

def get_real_ip(request):
    """Get the real IP address, handling proxies and load balancers"""
    # Check for IP behind proxies
    if request.environ.get('HTTP_CF_CONNECTING_IP'):
        return request.environ.get('HTTP_CF_CONNECTING_IP')
    
    if request.environ.get('HTTP_X_FORWARDED_FOR'):
        return request.environ.get('HTTP_X_FORWARDED_FOR').split(',')[0].strip()
    
    if request.environ.get('HTTP_X_FORWARDED'):
        return request.environ.get('HTTP_X_FORWARDED')
    
    if request.environ.get('HTTP_FORWARDED_FOR'):
        return request.environ.get('HTTP_FORWARDED_FOR')
    
    if request.environ.get('HTTP_FORWARDED'):
        return request.environ.get('HTTP_FORWARDED')
    
    # Default to remote_addr
    return request.remote_addr

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/collect', methods=['POST'])
def collect():
    data = request.get_json()
    
    # Get real IP address
    real_ip = get_real_ip(request)
    
    # Hostname lookup
    try:
        hostname = socket.gethostbyaddr(real_ip)[0]
    except:
        hostname = "Unknown"

    log = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "username": data.get("username", "Unknown"),
        "device": data.get("device"),
        "platform": data.get("platform"),
        "screen": data.get("screen"),
        "location": data.get("location"),
        "real_ip": real_ip,
        "hostname": hostname,
        "language": data.get("language"),
        "timezone": data.get("timezone"),
        "browser_name": data.get("browser_name")
    }

    logs.append(log)
    print(f"[LOG] {log}")  # Print to console for debugging

    return jsonify({"status": "ok"})

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', logs=logs)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
