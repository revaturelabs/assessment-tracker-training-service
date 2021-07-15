from flask import Flask
from flask_cors import CORS
from flask_restx import Api

from controllers import app_controller

app = Flask(__name__)
CORS(app)

# OpenAPI runs on default server link
# Lists all of our endpoints separated into Admin and Instructor categories
api = Api(app, version='1.0', title='Assessment-Tracker-Python-Endpoints',
          description="The Assessment Tracker is an application designed to help track an individual's progress through a batch training. A user can see all the batches organized by year, view a particular week for a batch, create new assessments, and organize assessments into types. Each assessment is assigned a weight to contribute to the final grade, and associates that complete a given assignment are given a grade in the application.",
          )
# Admin Namespace
ans = api.namespace(name='Admin', path='/', description='Admin related operations')
# Instructor Namespace
ins = api.namespace(name='Instructor', path='/', description='Instructor related operations')
# Use ans to switch to admin tab and ins for instructor tab respectively.
app_controller.route(ans, ins)

if __name__ == '__main__':
    app.run(debug=False)
