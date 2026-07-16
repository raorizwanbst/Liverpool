"""
Intentionally insecure code to exercise Semgrep (SAST) rules. Test fixture only —
every function here is a deliberate anti-pattern, do not copy into real code.
"""
import hashlib
import os
import pickle
import sqlite3
import subprocess

import requests
import yaml
from flask import Flask, request

app = Flask(__name__)


@app.route("/eval")
def eval_endpoint():
    # code injection: eval on user input
    expr = request.args.get("expr", "")
    return str(eval(expr))


@app.route("/exec")
def exec_endpoint():
    exec(request.args.get("code", ""))          # code injection
    return "ok"


@app.route("/ping")
def ping():
    host = request.args.get("host", "")
    # command injection: shell=True with user input
    return subprocess.check_output(f"ping -c 1 {host}", shell=True)


@app.route("/run")
def run():
    os.system("rm -rf /tmp/" + request.args.get("path", ""))   # command injection
    return "ok"


def load_config(blob: bytes):
    # insecure deserialization
    cfg = yaml.load(blob, Loader=yaml.Loader)
    return pickle.loads(blob)


def get_user(user_id: str):
    conn = sqlite3.connect("app.db")
    # SQL injection: string-built query
    return conn.execute("SELECT * FROM users WHERE id = '%s'" % user_id).fetchall()


def fetch(url: str):
    # TLS verification disabled
    return requests.get(url, verify=False)


def weak_hash(password: str) -> str:
    # weak hashing algorithm
    return hashlib.md5(password.encode()).hexdigest()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")          # debug server bound to all interfaces
