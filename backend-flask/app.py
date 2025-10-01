from flask import Flask, request
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
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception

# JWT + Requests (for Cognito token validation)
import jwt
import requests
from functools import wraps

# ---------------- Flask app ----------------
app = Flask(__name__)

# ---------------- CloudWatch Logger ----------------
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
cw_handler = watchtower.CloudWatchLogHandler(log_group="cruddur")
LOGGER.addHandler(console_handler)
LOGGER.addHandler(cw_handler)
LOGGER.info("CloudWatch Logs initialized ✅")

# ---------------- Honeycomb (OTel) ----------------
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
simple_processor = SimpleSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(simple_processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

# ---------------- X-Ray ----------------
xray_url = os.getenv("AWS_XRAY_URL")
xray_recorder.configure(service="backend-flask", dynamic_naming=xray_url)
XRayMiddleware(app, xray_recorder)

# Auto-instrument Flask + requests for OTel
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

# ---------------- CORS ----------------
frontend = os.getenv("FRONTEND_URL")
backend = os.getenv("BACKEND_URL")
origins = [frontend, backend]

CORS(
    app,
    resources={r"/api/*": {"origins": origins}},
    supports_credentials=True,
    expose_headers=["Authorization", "Location", "Link"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
    methods="OPTIONS,GET,HEAD,POST,PUT,DELETE"
)

# ---------------- Rollbar init ----------------
rollbar_access_token = os.getenv("ROLLBAR_ACCESS_TOKEN") or ""
if rollbar_access_token:
    rollbar.init(
        rollbar_access_token,
        "production",
        root=os.path.dirname(os.path.realpath(__file__)),
        allow_logging_basic_config=False,
    )
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)

@app.route("/rollbar/test")
def rollbar_test():
    rollbar.report_message("Hello World!", "warning")
    return "Hello World!"

# ---------------- Cognito JWT Validation ----------------
COGNITO_REGION = os.getenv("AWS_COGNITO_REGION")
USERPOOL_ID = os.getenv("AWS_COGNITO_USERPOOL_ID")

def get_jwks():
    if not COGNITO_REGION or not USERPOOL_ID:
        print("Warning: Cognito environment variables not set")
        return None
    try:
        jwks_url = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USERPOOL_ID}/.well-known/jwks.json"
        response = requests.get(jwks_url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Failed to fetch JWKS: {e}")
        return None

jwks = get_jwks()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return {"error": "Token missing"}, 401

        if not jwks:
            print("Warning: JWKS not available, skipping token validation")
            request.user = {"username": "test_user"}
            return f(*args, **kwargs)

        try:
            header = jwt.get_unverified_header(token)
            key = next(k for k in jwks["keys"] if k["kid"] == header["kid"])
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)

            decoded = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                issuer=f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USERPOOL_ID}",
                audience="cte794vg6jirnr3eqtt2v500i"
            )
            request.user = decoded
        except Exception as e:
            print(f"Token validation error: {e}")
            return {"error": f"Invalid token: {str(e)}"}, 401

        return f(*args, **kwargs)
    return decorated

# ---------------- Routes ----------------

@app.route("/api/activities/home", methods=["GET"])
@cross_origin()
@xray_recorder.capture("activities_home")
@token_required
def data_home():
    with tracer.start_as_current_span("custom.activities_home") as span:
        span.set_attribute("user.handle", "test_user")
        data = HomeActivities.run()
        span.set_attribute("result.count", len(data) if data else 0)
        return data, 200

@app.route("/api/activities/notifications", methods=["GET"])
@cross_origin()
def data_notifications():
    data = [
        {
            'uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eee',
            'handle': 'coco',
            'message': 'I am a white unicorn',
            'created_at': '2023-03-01T21:12:19.000Z',
            'expires_at': '2023-03-08T21:12:19.000Z'
        }
    ]
    return data, 200

@app.route("/api/activities/@<string:handle>", methods=["GET"])
@cross_origin()
@xray_recorder.capture("activities_users")
def data_handle(handle):
    model = UserActivities.run(handle)
    if model["errors"] is not None:
        return model["errors"], 422
    else:
        return model["data"], 200

@app.route("/api/message_groups", methods=['GET'])
@cross_origin()
def data_message_groups():
    user_handle = 'andrewbrown'
    model = MessageGroups.run(user_handle=user_handle)
    if model['errors'] is not None:
        return model['errors'], 422
    else:
        return model['data'], 200

@app.route("/api/messages/@<string:handle>", methods=['GET'])
@cross_origin()
def data_messages(handle):
    user_sender_handle = 'andrewbrown'
    user_receiver_handle = request.args.get('user_reciever_handle')
    model = Messages.run(user_sender_handle=user_sender_handle, user_receiver_handle=user_receiver_handle)
    if model['errors'] is not None:
        return model['errors'], 422
    else:
        return model['data'], 200

@app.route("/api/messages", methods=['POST','OPTIONS'])
@cross_origin()
def data_create_message():
    user_sender_handle = 'andrewbrown'
    user_receiver_handle = request.json['user_receiver_handle']
    message = request.json['message']
    model = CreateMessage.run(message=message,user_sender_handle=user_sender_handle,user_receiver_handle=user_receiver_handle)
    if model['errors'] is not None:
        return model['errors'], 422
    else:
        return model['data'], 200

@app.route("/api/activities/search", methods=['GET'])
@cross_origin()
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
    user_handle = 'andrewbrown'
    message = request.json['message']
    ttl = request.json['ttl']
    model = CreateActivity.run(message, user_handle, ttl)
    if model['errors'] is not None:
        return model['errors'], 422
    else:
        return model['data'], 200

@app.route("/api/activities/<string:activity_uuid>", methods=['GET'])
@cross_origin()
@xray_recorder.capture("activities_show")
def data_show_activity(activity_uuid):
    data = ShowActivity.run(activity_uuid=activity_uuid)
    return data, 200

@app.route("/api/activities/<string:activity_uuid>/reply", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities_reply(activity_uuid):
    user_handle = 'andrewbrown'
    message = request.json['message']
    model = CreateReply.run(message, user_handle, activity_uuid)
    if model['errors'] is not None:
        return model['errors'], 422
    else:
        return model['data'], 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4567, debug=True)
