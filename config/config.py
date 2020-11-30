# encoding=utf8
import os


class Config(object):
    # 主机ip地址
    # HOST = '0.0.0.0'
    HOST = '127.0.0.1'
    PORT = 5000
    SCHEDULER_API_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    DEBUG = False

    MYSQL_HOST = 'host'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASS = 'pwd'
    MYSQL_DB = 'python-tool'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8".format(
        MYSQL_USER,
        MYSQL_PASS,
        MYSQL_HOST,
        MYSQL_PORT,
        MYSQL_DB
    )
    GRAB_MEETING_TRY_TIMES = 30
    REDIS_URL = 'redis://:pwd@host:6379/10'


class DevConfig(Config):
    DEBUG = True

    MYSQL_HOST = 'host'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASS = 'pwd'
    MYSQL_DB = 'python-tool'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8".format(
        MYSQL_USER,
        MYSQL_PASS,
        MYSQL_HOST,
        MYSQL_PORT,
        MYSQL_DB
    )
    GRAB_MEETING_TRY_TIMES = 1
    REDIS_URL = 'redis://:pwd@host:6379/10'


# Default using Config settings, you can write if/else for different env
if os.getenv('PYTHON_ENV') == 'production':
    config = ProdConfig()
else:
    config = DevConfig()
