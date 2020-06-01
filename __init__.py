from flask import Flask

app = Flask(__name__)

from .api.routes import api_mod
from .site.routes import site_mod

app.register_blueprint(api.routes.api_mod, url_prefix='/api/v1.0')
app.register_blueprint(site.routes.site_mod)