from models.trainer import Trainer
from flask import request, jsonify

from exceptions.resource_not_found import ResourceNotFound
from services.trainer_service import TrainerService
from utils.json_tool import convert_list_to_json

import json

INVALID_ID_ERROR = "Not a valid ID or No such batch exist with this ID"


def route(app):

    @app.route("/login", methods=["POST"])
    def login():
        try:
            email = request.json["email"]
            return jsonify(TrainerService.login(email).json())
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/trainers/<trainer_id>", methods=["GET"])
    def get_trainer_by_id(trainer_id):
        try:
            return jsonify(
                TrainerService.get_trainer_by_id(int(trainer_id)).json())
        except ValueError:
            return INVALID_ID_ERROR, 400  # Bad Request
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/batches/<batch_id>/trainers", methods=["GET"])
    def get_trainers_by_batch_id(batch_id):
        try:
            trainers = TrainerService.get_trainers_in_batch(int(batch_id))
        except ValueError:
            return INVALID_ID_ERROR, 400  # Bad Request
        except ResourceNotFound as r:
            return r.message, 404
        trainers_as_json = convert_list_to_json(trainers)
        return jsonify(trainers_as_json)

    # /years?trainer_id=<trainer_id>
    @app.route("/years", methods=["GET"])
    def get_years_for_trainer():
        trainer_id = request.args.get("trainerId")
        if trainer_id is not None:
            try:
                return jsonify(
                    TrainerService.get_years_for_trainer(int(trainer_id)))
            except ValueError:
                return INVALID_ID_ERROR, 400  # Bad Request
        else:
            return jsonify([])

    @app.route("/trainers", methods=["POST"])
    def post_trainer():
        """Create a new trainer.
        Accepts a JSON input:
        {
            "firstName": str,
            "lastName": str,
            "email": str
        }
        """
        try:
            body = json.loads(request.data.decode("utf-8"))
            trainer = Trainer(body["firstName"], body["lastName"],
                              body["email"])
            trainer = TrainerService.create_trainer(trainer)
            return jsonify(trainer.json()), 201
        except ValueError:
            return INVALID_ID_ERROR, 400  # Bad Request
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/trainers/register", methods=["POST"])
    def post_trainer_batch():
        """
        Create a new trainer-batch join relationship

        Accepts a JSON input:
        {
            "trainerId": int,
            "batchId": int,
            "trainerRole": str
        }
        """
        try:
            body = json.loads(request.data.decode("utf-8"))
            trainer = TrainerService.get_trainer_by_id(body["trainerId"])
            trainer.role = body["trainerRole"]
            register = TrainerService.assign_trainer_to_batch(
                trainer, body["batchId"])
            return jsonify(register.json()), 201
        except (ValueError):
            return INVALID_ID_ERROR, 400
        except (KeyError, TypeError):
            return "Invalid JSON body", 400
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/trainers", methods=["GET"])
    def get_all_trainers():
        try:
            return jsonify(TrainerService.get_all_trainers())
        except ResourceNotFound as r:
            return r.message, 404

