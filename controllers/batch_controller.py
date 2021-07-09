import datetime
import psycopg2
from flask import jsonify, request

from exceptions.resource_not_found import ResourceNotFound
from models.batch import Batch
from services.batch_services import BatchServices
from utils.json_tool import convert_list_to_json

INVALID_ID_ERROR = "Not a valid ID or No such batch exist with this ID"


def route(app):
    @app.route("/batch", methods=["POST"])
    def create_batch():
        """Creates a Batch object using inputs from JSON"""
        # General date format example: "2021-12-19"
        try:
            body = request.json
            batch = Batch(body["name"], body["trainingTrack"], body["startDate"], body["endDate"])
            result = BatchServices.create_batch(batch)
            return f"Batch [{body['name']}] successfully created with an id of {result.id}", 201
        except psycopg2.errors.InvalidDatetimeFormat:
            return f"Start date or end date are not valid date", 400  # Bad Request

    @app.route("/batch/<id>/", methods=["GET"])
    def get_batch_by_id(id):
        """Takes in an id for a batch record and returns a Batch object"""
        try:
            return jsonify(BatchServices.get_batch_by_id(int(id)).json())
        except ValueError:
            return INVALID_ID_ERROR, 400  # Bad Request
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/batches/<trainer_id>/<year>/", methods=["GET"])
    def get_all_batches_by_year(trainer_id, year):
        """Takes in a year and returns all the batches currently in progress for that year"""
        try:
            batches = BatchServices.get_all_batches_by_year(int(trainer_id), int(year))
        except ValueError:
            return INVALID_ID_ERROR, 400  # Bad Request
        batches_as_json = convert_list_to_json(batches)
        return jsonify(batches_as_json)

    @app.route("/batches/search/<trainer_id>/<track>/", methods=["GET"])
    def search_for_batch(trainer_id, track):
        try:
            batches = BatchServices.search_for_batch(int(trainer_id), track)
        except ValueError:
            return INVALID_ID_ERROR, 400  # Bad Request
        batches_as_json = convert_list_to_json(batches)
        return jsonify(batches_as_json)
