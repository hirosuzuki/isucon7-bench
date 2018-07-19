from flask import Flask, render_template, Response, request

import json
import time
import random

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

@app.route("/users")
def users():
    page = auth.list_users()
    users = []
    while page:
        for user in page.users:
            users.append(user.email)
        page = page.get_next_page()
    return Response(json.dumps(users), mimetype="application/json")

@app.route("/tasks")
def tasks():
    db = firestore.client()
    doc_ref = db.collection(u'tasks').document(u'id')
    data = doc_ref.get()
    return Response(json.dumps(data.to_dict()), mimetype="application/json")

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

@app.route("/bench", methods=['POST'])
def bench():
    def run():
        p = Popen([
                "/home/isucon/isubata/bench/bin/bench",
                "-remotes",
                "104.198.80.0:80",
                "-data",
                "/home/isucon/isubata/bench/data/",
                "-output",
                "/tmp/1.json"
            ], stdout=PIPE, stderr=PIPE
            )
        for line in p.stderr:
            yield line
    return Response(run(), mimetype="text/plain")

@app.route("/token", methods=['POST'])
def req():
    idToken = request.headers.get("X-ID-TOKEN", "")
    decoded_token = auth.verify_id_token(idToken)
    print(decoded_token)
    uid = decoded_token['uid']
    return "OK"

if __name__ == "__main__":
    app.run(debug=True)
