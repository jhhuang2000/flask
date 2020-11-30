# encoding=utf8
from flask import g
from flask_httpauth import HTTPTokenAuth
import json
from config.redis import redis_client

auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):
    g.user = None
    user = redis_client.get(token)
    if user:
        g.user = json.loads(user)
        return True
    else:
        return False
