from flask import request
from flask_restx import Resource

from exceptions.resource_not_found import ResourceNotFound
from services.trainer_service import TrainerService
from utils.json_tool import convert_list_to_json

INVALID_ID_ERROR = "Not a valid ID or No such batch exist with this ID"


def route(ans, ins):
    @ans.route('/trainers')
    @ans.response(404, "No user with those credentials")
    class Login(Resource):
        def post(self):
            try:
                email = request.json["email"]
                return TrainerService.login(email).json()
            except ResourceNotFound as r:
                return r.message, 404

    @ins.route('/trainers/<trainer_id>')
    @ins.param('trainer_id', "Trainer ID")
    @ins.response(400, "Bad Request")
    @ins.response(404, "No Trainer with that ID")
    class GetTrainerById(Resource):
        def get(self, trainer_id):
            try:
                return TrainerService.get_trainer_by_id(int(trainer_id)).json()
            except ValueError:
                return INVALID_ID_ERROR, 400  # Bad Request
            except ResourceNotFound as r:
                return r.message, 404

    @ins.route('/batches/<batch_id>/trainers')
    @ins.param('batch_id', "Batch ID of the batch you want trainer")
    @ins.response(400, "Bad Request")
    @ins.response(404, 'No trainers associated with that Batch')
    class GetTrainersInBatch(Resource):
        def get(self, batch_id):
            try:
                trainers = TrainerService.get_trainers_in_batch(int(batch_id))
            except ValueError:
                return INVALID_ID_ERROR, 400  # Bad Request
            except ResourceNotFound as r:
                return r.message, 404
            trainers_as_json = convert_list_to_json(trainers)
            return trainers_as_json

    @ins.route('/years')
    @ins.response(400, "Invalid ID")
    class GetYearsForTrainer(Resource):
        def get(self):
            trainer_id = request.args.get("trainerId")
            if trainer_id is not None:
                try:
                    return TrainerService.get_years_for_trainer(int(trainer_id))
                except ValueError:
                    return INVALID_ID_ERROR, 400  # Bad Request
            else:
                return []
