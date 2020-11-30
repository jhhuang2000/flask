# encoding=utf8
from flask_sqlalchemy import SQLAlchemy
import datetime
import json
import decimal

db = SQLAlchemy()


class DbBase(db.Model):
    __abstract__ = True

    @staticmethod
    def date_encode(obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, datetime.time):
            return obj.strftime('%H:%M')
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        else:
            return obj

    def to_dict(self):
        return {c.key: self.date_encode(getattr(self, c.key)) for c in self.__table__.columns}
