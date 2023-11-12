# import logging
from flask import Flask

from apps.routes import apps

from flask_cors import CORS

app = Flask(__name__)

# logging.basicConfig(level=logging.DEBUG)

app.register_blueprint(apps)

# 如果 nginx 中配置了 Access-Origin，则这里不需要开启CORS
# CORS(app)

if __name__ == '__main__':
    # app.config['DEBUG'] = True
    app.run(host='0.0.0.0', port=5000)
