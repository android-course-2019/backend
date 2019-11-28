from flask import Flask
from flask_session import Session
from config.flask_app_config import config

app = Flask(__name__)
app.config.update(config)

Session(app)

from application.services import *
from application.domains import *
from application.controllers import *
