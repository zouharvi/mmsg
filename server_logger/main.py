#!/usr/bin/env python3

from flask import Flask, request
import json
from flask_cors import CORS, cross_origin
from waitress import serve
import os
import datetime

app = Flask(__name__)
CORS(app)

os.makedirs("logs", exist_ok=True)

@app.route("/log", methods=["GET", "POST"])
def action_log():
    data = request.get_json()
    uid = data.pop("uid")
    print(f"[{datetime.datetime.now()}] log equest from user {uid}")
    if uid.replace("_", "").isalnum() and len(uid) <= 50:
        with open(f"logs/{uid}.jsonl", "a") as f:
            f.write(json.dumps(data) + "\n")

    return json.dumps({'success': 'ok'})

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=80)