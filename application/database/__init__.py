from flask_sqlalchemy import SQLAlchemy
from application.config.private_data import db_connection_info
from application import app

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql://{username}:{password}@{host}/{db_name}'.format(**db_connection_info)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

from application.database.models import *
from application.database.relations import *
