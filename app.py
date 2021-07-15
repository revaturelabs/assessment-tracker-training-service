from flask import Flask
from flask_cors import CORS
from flask_restx import Api

from controllers import app_controller

app = Flask(__name__)
CORS(app)
api = Api(app)
app_controller.route(api)

if __name__ == '__main__':
    app.run(debug=False)
