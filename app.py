from flask import Flask, request, render_template, jsonify
from datetime import datetime

app = Flask(__name__)

logs = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/collect", methods=["POST"])
def collect():
    data = request.json

    log = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "device": data.get("device"),
        "platform": data.get("platform"),
        "screen": data.get("screen"),
        "location": data.get("location"),
        "note": "User consented"
    }

    logs.append(log)
    return jsonify({"status": "ok"})

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", logs=logs[::-1])

if __name__ == "__main__":
    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port))