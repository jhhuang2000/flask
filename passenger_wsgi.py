from manage import app as application
from werkzeug.debug import DebuggedApplication

application = DebuggedApplication(application, evalex=True)
