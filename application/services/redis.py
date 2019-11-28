from redis import Redis

from config.private_data import redis_connection_info

redis = Redis(**redis_connection_info, decode_responses=False)
