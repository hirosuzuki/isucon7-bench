from flask import Flask, render_template, Response, request

import json
import time
import random
import re
import os

import firebase_admin
from firebase_admin import credentials, auth, firestore, db

app = Flask(__name__)

cred = credentials.Certificate('firebase-secret.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://isucon-bench.firebaseio.com/'
})

@app.route("/")
def home():
    return open('templates/home.html').read()

CHARS = "0123456789ABCDEF"

@app.route("/request", methods=['POST'])
def request_task():
    jobid = "".join(random.choice(CHARS) for i in range(48))
    email = request.json.get("email")
    server = request.json.get("server")
    now = int(time.time())

    data = {
        'jobid': jobid,
        'email': email,
        'server': server,
        'posttime': now,
        'starttime': None,
        'endtime': None,
        'status': 0,
        'score': 0,
    }

    tasks_ref = db.reference('tasks')
    tasks = tasks_ref.get()
    if tasks:
        for key, task in tasks.items():
            if task.get("server") == server and task.get("status") == 0:
                tasks_ref.child(key).set({})

    new_task_ref = tasks_ref.push()
    new_task_ref.set(data)

    return Response("OK", mimetype="application/json")

@app.route("/result/<jobid>")
def view_result(jobid):
    if not re.match(r'^[0123456789ABCDEF]+$', jobid):
        return "-"
    result_filename = "/var/isucon7/%s.json" % jobid
    if not os.path.exists(result_filename):
        return "-"
    result = json.load(open(result_filename))
    return render_template("result.html", result=result)
    return Response(json.dumps(result, indent=2), mimetype="application/json")

if __name__ == "__main__":
    app.run(debug=True)
