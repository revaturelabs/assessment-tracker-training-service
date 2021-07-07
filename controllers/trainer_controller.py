from flask import request, jsonify

from exceptions.resource_not_found import ResourceNotFound
from services.trainer_service import TrainerService
from utils.json_tool import convert_list_to_json

INVALID_ID_ERROR = "Not a valid ID or No such batch exist with this ID"

def route(app):
    @app.route("/trainer/", methods=["POST"])
    def login():
        try:
            email = request.json["email"]
            return jsonify(TrainerService.login(email).json())
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/trainer/<id>/", methods=["GET"])
    def get_trainer_by_id(id):
        try:
            return jsonify(TrainerService.get_trainer_by_id(int(id)).json())
        except ValueError:
            return INVALID_ID_ERROR, 400  # Bad Request
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/trainers/<batch_id>/", methods=["GET"])
    def get_trainers_by_batch_id(batch_id):
        try:
            trainers = TrainerService.get_trainers_in_batch(int(batch_id))
        except ValueError:
            return INVALID_ID_ERROR, 400  # Bad Request
        except ResourceNotFound as r:
            return r.message, 404
        trainers_as_json = convert_list_to_json(trainers)
        return jsonify(trainers_as_json)

    @app.route("/trainers/years/<trainer_id>", methods=["GET"])
    def get_years_for_trainer(trainer_id):
        try:
            return jsonify(TrainerService.get_years_for_trainer(int(trainer_id)))
        except ValueError:
            return INVALID_ID_ERROR, 400  # Bad Request
