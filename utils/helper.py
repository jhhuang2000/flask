# encoding=utf8
from flask import Response, jsonify, request
import datetime
import json
import decimal


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, datetime.time):
            return obj.strftime('%H:%M')
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        else:
            return json.JSONEncoder.default(self, obj)


def my_dump(data):
    return json.dumps(data, cls=DateEncoder)


def as_json(code=1, msg='', data={}):
    '''
    return Response(
        json.dumps({'code': code, 'msg': msg, 'data': data}, cls=DateEncoder),
        content_type='application/json'
    )
    '''
    return jsonify({'code': code, 'msg': msg, 'data': data})


def success_return(data={}, msg='操作成功'):
    return as_json(1, msg, data)


def error_return(msg='操作失败', data={}):
    return as_json(0, msg, data)


def object_to_dict(obj):
    return {c.key: getattr(obj, c.key) for c in obj.__table__.columns}


def objects_to_dict(objs):
    return [object_to_dict(obj) for obj in objs]


def list_return(query):
    page = int(request.values.get('page', 1))
    page_size = int(request.values.get('page_size', 20))
    offset = (page - 1) * page_size
    lists = [obj.to_dict() for obj in query.offset(offset).limit(page_size).all()]
    return success_return({'lists': lists, 'count': str(query.count())})
