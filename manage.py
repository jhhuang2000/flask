# encoding=utf8
from flask_script import Manager, Server
from flask_apidoc.commands import GenerateApiDoc
from app import create_app

app = create_app()
app.debug = app.config['DEBUG']
host = app.config['HOST']
port = app.config['PORT']

manager = Manager(app)
manager.add_command('apidoc', GenerateApiDoc())
manager.add_command('run', Server(host=host, port=port, threaded=True))

if __name__ == '__main__':
    manager.run()
