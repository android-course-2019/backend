from flask_sqlalchemy import SQLAlchemy
from application import app


db = SQLAlchemy(app)

from application.database.models import *
from application.database.relations import *
