from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

from controllers import app_controller

app = Flask(__name__)
app_controller.route(app)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Assessment-Tracker-Python-Endpoints"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix = SWAGGER_URL)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
