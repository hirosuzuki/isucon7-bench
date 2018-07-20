import firebase_admin
from firebase_admin import credentials, db
from time import sleep
import time
from subprocess import Popen, PIPE, call
import json

cred = credentials.Certificate('firebase-secret.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://isucon-bench.firebaseio.com/'
})

def fetch_tasks():
    tasks_ref = db.reference('tasks')
    tasks = tasks_ref.get()
    waiting_tasks = []
    for key, task in tasks.items():
        if task.get("status") == 0:
            task["key"] = key
            waiting_tasks.append((key, task))
    waiting_tasks.sort(key=lambda x:x[1].get("posttime"))
    return waiting_tasks

def run(jobid, server):
    output_filename = "/var/isucon7/%s.json" % jobid
    cmd = [
        "/home/isucon/isubata/bench/bin/bench",
        "-remotes", server,
        "-data", "/home/isucon/isubata/bench/data/",
        "-output", output_filename
    ]
    retcode = call(cmd)
    if retcode != 0:
        return -1
    result = json.load(open(output_filename))
    return result.get("score")

def execute_task(key, task):
    print("Execute Task: %s" % key)
    tasks_ref = db.reference('tasks')
    task_ref = tasks_ref.child(task["key"])
    data = task_ref.get()
    data["status"] = 1
    data["starttime"] = int(time.time())
    task_ref.set(data)
    score = run(task["jobid"], task["server"])
    print("Execute Task Done: %s %s" % (key, score))
    data["status"] = 2
    data["score"] = score
    data["endtime"] = int(time.time())
    task_ref.set(data)

while 1:
    waiting_tasks = fetch_tasks()
    if waiting_tasks:
        key, task = waiting_tasks[0]
        execute_task(key, task)
        sleep(3)
    else:
        print("polling ...")
        sleep(15)

