from flask import Flask, g
from uuid import uuid4
app = Flask(__name__)

@app.route("/")
def landing_page():
    return "App Flask. Permet de generer les metriques pour le projet \n - /error = err 500\n - /ok = OK 200"

@app.route("/ok")
def return_valid():
    return "OK", 200

@app.route("/error")
def return_error():
    return "err", 500

@app.route("/metrics")
def return_metrics():
    return "metrics"

@app.before_request
def before_request():
  g.request_id = str(uuid4())





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)