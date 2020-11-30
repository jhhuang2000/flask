# encoding=utf8
import os
import logging
from config.config import config


def init_app(app):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logger_path = '{0}/logs'.format(BASE_DIR)
    if not os.path.exists(logger_path):
        os.mkdir(logger_path)

    handler = logging.FileHandler(logger_path + "/{0}.log".format(config.MYSQL_DB), encoding='UTF-8')
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s'
    )
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)


