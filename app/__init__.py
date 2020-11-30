# encoding=utf8
from flask import Flask, jsonify
from flask_cors import CORS
from flask_apidoc import ApiDoc
from config.config import config
from config.error import BaseError, OrmError
from config import urls, logger, scheduler, redis
from models import db
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_app():
    app = Flask(__name__, root_path=BASE_DIR)
    CORS(app, resources={r'/*': {"origins": "*"}})

    app.config.from_object(config)

    # 注册apidoc
    doc = ApiDoc(app=app)
    # 注册logger
    logger.init_app(app)
    # 注册路由
    urls.register(app)
    # 注册数据库
    db.init_app(app)
    db.app = app
    # 注册schedules
    scheduler.init_app(app)
    # 注册redis
    redis.init_app(app)

    @app.errorhandler(BaseError)
    def custom_error_handler(e):
        if e.level in [BaseError.LEVEL_WARN, BaseError.LEVEL_ERROR]:
            if isinstance(e, OrmError):
                app.logger.exception('%s %s' % (e.parent_error, e))
            else:
                app.logger.exception('错误信息: %s %s' % (e.extras, e))
        app.logger.error('Common error: %s', e)
        response = jsonify(e.to_dict())
        response.status_code = e.status_code
        return response

    return app
