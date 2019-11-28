from .private_data import db_connection_info, flask_secret_key
from application.services.redis import redis

config = {
    'SQLALCHEMY_DATABASE_URI': 'mysql://{username}:{password}@{host}/{db_name}'.format(**db_connection_info),
    'SQLALCHEMY_TRACK_MODIFICATIONS': True,
    'SESSION_TYPE': 'redis',
    'SESSION_USE_SIGNER': True,
    'SECRET_KEY': flask_secret_key,
    'SESSION_REDIS': redis
}
