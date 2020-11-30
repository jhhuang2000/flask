# encoding=utf8

from werkzeug.routing import BaseConverter
from app.task import task


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


def register(app):
    app.url_map.converters['regex'] = RegexConverter
    app.register_blueprint(task, url_prefix='/task', strict_slashes=False)
