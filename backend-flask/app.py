from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import os

from services.home_activities import *
from services.user_activities import *
from services.create_activity import *
from services.create_reply import *
from services.search_activities import *
from services.message_groups import *
from services.messages import *
from services.create_message import *
from services.show_activity import *

# HoneyComb ---------
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

# X-RAY ----------
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

# CloudWatch Logs ----
import watchtower
import logging

# Rollbar ------
from time import strftime
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception

# ---------------- Flask app ----------------
app = Flask(__name__)

# ---------------- CloudWatch Logger ----------------
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

# Send logs to both console and CloudWatch
console_handler = logging.StreamHandler()
cw_handler = watchtower.CloudWatchLogHandler(log_group="cruddur")

LOGGER.addHandler(console_handler)
LOGGER.addHandler(cw_handler)

# Test log to confirm CloudWatch works
LOGGER.info("CloudWatch Logs initialized ✅")

# ---------------- Honeycomb (OTel) ----------------
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)

# Also print spans to console (dev-friendly)
simple_processor = SimpleSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(simple_processor)

trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

# X-Ray ----------
xray_url = os.getenv("AWS_XRAY_URL")
xray_recorder.configure(service='backend-flask', dynamic_naming=xray_url)
XRayMiddleware(app, xray_recorder)

# Auto-instrument Flask + requests for OTel
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

# ---------------- CORS ----------------
frontend = os.getenv('FRONTEND_URL')
backend = os.getenv('BACKEND_URL')
origins = [frontend, backend]
cors = CORS(
  app,
  resources={r"/api/*": {"origins": origins}},
  expose_headers="location,link",
  allow_headers="content-type,if-modified-since",
  methods="OPTIONS,GET,HEAD,POST"
)

# ---------------- Rollbar init (Option 2: immediate init) ----------------
rollbar_access_token = os.getenv('ROLLBAR_ACCESS_TOKEN') or ""

if rollbar_access_token:
    rollbar.init(
        rollbar_access_token,
        'production',
        root=os.path.dirname(os.path.realpath(__file__)),
        allow_logging_basic_config=False
    )
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)

@app.route('/rollbar/test')
def rollbar_test():
    rollbar.report_message('Hello World!', 'warning')
    return "Hello World!"

# ---------------- Routes ----------------
@app.route("/api/message_groups", methods=['GET'])
def data_message_groups():
  user_handle  = 'oshimthakur'
  model = MessageGroups.run(user_handle=user_handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/messages/@<string:handle>", methods=['GET'])
def data_messages(handle):
  user_sender_handle = 'oshimthakur'
  user_receiver_handle = request.args.get('user_reciever_handle')
  model = Messages.run(user_sender_handle=user_sender_handle, user_receiver_handle=user_receiver_handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/messages", methods=['POST','OPTIONS'])
@cross_origin()
def data_create_message():
  user_sender_handle = 'oshimthakur'
  user_receiver_handle = request.json['user_receiver_handle']
  message = request.json['message']
  model = CreateMessage.run(message=message,user_sender_handle=user_sender_handle,user_receiver_handle=user_receiver_handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

# ✅ Add X-Ray capture here
@app.route("/api/activities/home", methods=['GET'])
@xray_recorder.capture("activities_home")
def data_home():
  with tracer.start_as_current_span("custom.activities_home") as span:
      span.set_attribute("user.handle", "oshimthakur")
      span.set_attribute("route", "/api/activities/home")

      data = HomeActivities.run()
      span.set_attribute("result.count", len(data) if data else 0)

      return data, 200

# ✅ Add X-Ray capture here
@app.route("/api/activities/@<string:handle>", methods=['GET'])
@xray_recorder.capture("activities_users")
def data_handle(handle):
  model = UserActivities.run(handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/activities/search", methods=['GET'])
def data_search():
  term = request.args.get('term')
  model = SearchActivities.run(term)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/activities", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities():
  user_handle  = 'oshimthakur'
  message = request.json['message']
  ttl = request.json['ttl']
  model = CreateActivity.run(message, user_handle, ttl)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

# ✅ Add X-Ray capture here
@app.route("/api/activities/<string:activity_uuid>", methods=['GET'])
@xray_recorder.capture("activities_show")
def data_show_activity(activity_uuid):
  data = ShowActivity.run(activity_uuid=activity_uuid)
  return data, 200

@app.route("/api/activities/<string:activity_uuid>/reply", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities_reply(activity_uuid):
  user_handle  = 'oshimthakur'
  message = request.json['message']
  model = CreateReply.run(message, user_handle, activity_uuid)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

if __name__ == "__main__":
  app.run(debug=True)
