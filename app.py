# import logging
from flask import Flask

from apps.routes import apps

from flask_cors import CORS

app = Flask(__name__)

# logging.basicConfig(level=logging.DEBUG)

CORS(app)

app.register_blueprint(apps)

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(host='0.0.0.0', port=5000)
