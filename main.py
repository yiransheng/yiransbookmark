import os
import sys
import logging


DEBUG = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')


# Add lib as primary libraries directory, with fallback to lib/dist
# and optionally to lib/dist.zip, loaded using zipimport.
lib_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'lib')
if lib_path not in sys.path:
    sys.path[0:0] = [
        lib_path,
    ]

# Append zip archives to path for zipimport
for filename in os.listdir(lib_path):
    if filename.endswith((".zip", ".egg")):
        sys.path.insert(0, "%s/%s" % (lib_path, filename))


from google.appengine.ext import admin
from werkzeug_debugger_appengine import get_debugged_app

from api import app


def enable_appstats(app):
    """Enables appstats middleware."""
    from google.appengine.ext.appstats.recording import \
        appstats_wsgi_middleware
    app.wsgi_app = appstats_wsgi_middleware(app.wsgi_app)


admin_app = admin.application

#enable_appstats(app)
if app.config['DEBUG']:
    app = get_debugged_app(app)
