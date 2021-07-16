import json

from flask import request, jsonify
from flask_restx import Resource, fields


from exceptions.resource_not_found import ResourceNotFound
from models.trainer import Trainer
from services.trainer_service import TrainerService
from utils.json_tool import convert_list_to_json

INVALID_ID_ERROR = "Not a valid ID or No such batch exist with this ID"


def route(ans, ins):
    trainer_data = ans.model('Schemas', {
        "id": fields.Integer(default=0, description="Trainers id"),
        "firstName": fields.String(default="Adam", description="Trainer's first name"),
        "lastName": fields.String(default="Ranieri", description="Trainers last name"),
        "email": fields.String(default="real@email.com", description="Trainer's email address"),
        "role": fields.String(default="Leader", description="Trainer's role in batch"),
        "admin": fields.Boolean(default = False, description = "Trainer's administration status")
    })
    email_data = ans.model('Schemas', {
        "email": fields.String(default="real@email.com", description="Trainer's email address")
    })
    trainer_batch = ans.model("Schemas",{
            "trainerId": fields.Integer(default = 1, description="Trainer ID"),
            "batchId": fields.Integer(default = 1, description="Batch ID"),
            "trainerRole": fields.String(default = "Leader", description="Trainer's role")
    })
    year_data = ans.model('Schemas', {
        "year": fields.Integer(default="2021", description="year")
    })

    @ans.route('/login')
    @ans.response(404, "No user with those credentials")

    class Login(Resource):
        @ans.expect(email_data)
        def post(self):
            """Logs in a trainer using their email address"""
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
        @ins.marshal_with(trainer_data, mask=None)
        def get(self, trainer_id):
            """Retrieve trainer information using their ID"""
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
        @ins.marshal_with(trainer_data, as_list=True, mask=None)
        def get(self, batch_id):
            """Retrieves all trainers associated in the batch with given ID"""
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
    @ins.doc(params={
        'trainerId': {'in': 'query', 'description': '1', 'type': 'integer'}
    })
    class GetYearsForTrainer(Resource):
        @ins.marshal_with(year_data, as_list=True, mask=None)
        def get(self):
            """Gets the number of active years for the trainer with ID in argument"""
            trainer_id = request.args.get("trainerId")
            if trainer_id is not None:
                try:
                    return TrainerService.get_years_for_trainer(int(trainer_id))
                except ValueError:
                    return INVALID_ID_ERROR, 400  # Bad Request
            else:
                return []


    @ans.route('/trainers')
    @ans.response(201, "Successful creation")
    @ans.response(400, "Bad Request")
    @ans.response(404, "Resource Not Found")
    class PostTrainer(Resource):
        @ans.expect(trainer_data)
        def post(self):
            """Creates a trainer with the given information"""
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

        @ans.marshal_with(trainer_data,as_list=True, mask=None)
        def get(self):
            """Retrieves all trainers"""
            try:
                return TrainerService.get_all_trainers()
            except ResourceNotFound as r:
                return r.message, 404

    @ans.route("/trainers/register")
    @ans.response(201, "Successfully registered batch")
    @ans.response(400, "Invalid ID")
    @ans.response(400, "Invalid Json body")
    @ans.response(404, "Resource not found")
    class PostTrainerBatch(Resource):

        def post(self):
            """
                    Create a new trainer-batch join relationship
                    """
            try:
                body = json.loads(request.data.decode("utf-8"))
                trainer = TrainerService.get_trainer_by_id(body["trainerId"])
                trainer.role = body["trainerRole"]
                register = TrainerService.assign_trainer_to_batch(
                    trainer, body["batchId"])
                return {"result": True}, 201
            except ValueError:
                return INVALID_ID_ERROR, 400
            except (KeyError, TypeError):
                return "Invalid JSON body", 400
            except ResourceNotFound as r:
                return r.message, 404




