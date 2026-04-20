from flask import Flask, g, request
from uuid import uuid4
import logging
from pythonjsonlogger import jsonlogger
from prometheus_client import Counter, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)
http_requests_total = Counter('http_requests_total', 'Total HTTP requests', ['status'])
http_requests_all_total = Counter('http_requests_all_total', 'Total HTTP requests')

logger = logging.getLogger("ynov-project-010")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    "%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s %(method)s %(path)s"
)
handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(handler)

logger.propagate = False
@app.route("/")
def landing_page():
    return "App Flask. Permet de generer les metriques pour le projet \n - /error = err 500\n - /ok = OK 200"

@app.route("/ok")
def return_valid():
    http_requests_total.labels(status='200').inc()
    logger.info(
        "Request handled successfully",
        extra={
            "request_id": g.request_id,
            "method": request.method,
            "path": request.path,
        },
    )
    return "OK", 200

@app.route("/error")
def return_error():
    http_requests_total.labels(status='500').inc()
    logger.error(
        "Request failed",
        extra={
            "request_id": g.request_id,
            "method": request.method,
            "path": request.path,
        },
    )
    return "err", 500

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

@app.before_request
def before_request():
  g.request_id = str(uuid4())
  http_requests_all_total.inc()
  logger.info(
      "Incoming request",
      extra={
          "request_id": g.request_id,
          "method": request.method,
          "path": request.path,
      },
  )





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)