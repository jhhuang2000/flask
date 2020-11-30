# encoding=utf8
from flask_redis import FlaskRedis

redis_client = FlaskRedis()


def init_app(app):
    redis_client.init_app(app)
