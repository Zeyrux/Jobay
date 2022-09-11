import mimetypes

from application.backend import App


mimetypes.add_type("application/javascript", ".js")
app = App()
application = app.app
application.debug = True
socket = app.socket