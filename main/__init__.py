import os

from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_compress import Compress
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask_apispec.extension import FlaskApiSpec


app = Flask(__name__)

app.config.from_pyfile("main.cfg")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config.update({
    "APISPEC_SPEC": APISpec(
        title="skeleton",
        version="v1",
        openapi_version="2.0.0",
        plugins=[MarshmallowPlugin()],

    ),
    "APISPEC_SWAGGER_URL": "/docs.json",
    "APISPEC_SWAGGER_UI_URL": "/docs/"
})


docs = FlaskApiSpec(app)
db = SQLAlchemy(app)
compress = Compress(app)
CORS(app)
api = Api(app)

# Blueprint
from main.controllers import bps

for bp in bps:
  app.register_blueprint(bp)
docs.register_existing_resources()

# 스웨거에서 options 제거
for key, value in docs.spec._paths.items():
  docs.spec._paths[key] = {
      inner_key: inner_value for inner_key, inner_value in value.items() if inner_key != "options"
  }
