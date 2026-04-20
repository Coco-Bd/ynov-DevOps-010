from flask import Flask, g
from uuid import uuid4
from prometheus_client import Counter, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)
http_requests_total = Counter('http_requests_total', 'Total HTTP requests', ['status'])
http_requests_all_total = Counter('http_requests_all_total', 'Total HTTP requests')
@app.route("/")
def landing_page():
    return "App Flask. Permet de generer les metriques pour le projet \n - /error = err 500\n - /ok = OK 200"

@app.route("/ok")
def return_valid():
    http_requests_total.labels(status='200').inc()
    return "OK", 200

@app.route("/error")
def return_error():
    http_requests_total.labels(status='500').inc()
    return "err", 500

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

@app.before_request
def before_request():
  g.request_id = str(uuid4())
  http_requests_all_total.inc()





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)