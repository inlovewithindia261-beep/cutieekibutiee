from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime

app = Flask(name)

logs = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/collect', methods=['POST'])
def collect():
    data = request.get_json()

    log = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "device": data.get("device"),
        "platform": data.get("platform"),
        "screen": data.get("screen"),
        "location": data.get("location"),
        "ip": request.remote_addr
    }

    logs.append(log)

    return jsonify({"status": "ok"})

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', logs=logs)

# 🔥 Railway fix
if name == "main":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
