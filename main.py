from flask import Flask, render_template, Response

import json

import firebase_admin
from firebase_admin import credentials, auth, firestore

app = Flask(__name__)

cred = credentials.Certificate('firebase-secret.json')
default_app = firebase_admin.initialize_app(cred)

@app.route("/")
def home():
    return render_template('home.html')

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
