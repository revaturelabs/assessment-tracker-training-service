import psycopg2
from flask import jsonify, request
from flask_restx import Resource, fields

from exceptions.resource_not_found import ResourceNotFound
from models.batch import Batch
from services.batch_services import BatchServices
from utils.json_tool import convert_list_to_json

INVALID_ID_ERROR = "Not a valid ID or No such batch exist with this ID"


def route(ans, ins):
    batch_data = ans.model('Schemas', {
        "name": fields.String(default="Reston-7152021", description='Name of the batch'),
        "trainingTrack": fields.String(default="Python, Java, Automation", description='Tech Stack for the batch'),
        "startDate": fields.Integer(default="1625843430", description='Epoch time in seconds'),
        "endDate": fields.Integer(default="1639008000", description='Epoch time in seconds')
    })

    @ans.route('/batches')
    @ans.response(201, "<batch_id>")
    @ans.response(400, 'Bad Request')
    class CreateBatch(Resource):
        @ans.expect(batch_data)
        def post(self):
            """Creates a Batch object using inputs from JSON"""
            try:
                body = request.json
                batch = Batch(body["name"], body["trainingTrack"], body["startDate"], body["endDate"])
                result = BatchServices.create_batch(batch)
                return jsonify(f"{result.id}"), 201
            except psycopg2.errors.InvalidDatetimeFormat as e:
                return str(e), 400  # Bad Request
            except ValueError as e:
                return str(e), 400

    @ins.route("/batches/<int:batch_id>")
    @ins.param('batch_id', 'Batch Unique Id')
    @ins.response(400, 'Bad Request')
    @ins.response(404, 'Resource not Found')
    class GetBatchById(Resource):
        @ins.marshal_with(batch_data, mask=None)
        def get(self, batch_id):
            """Takes in an id for a batch record and returns a Batch object"""
            try:
                return jsonify(BatchServices.get_batch_by_id(int(batch_id)).json())
            except ValueError:
                return INVALID_ID_ERROR, 400  # Bad Request
            except ResourceNotFound as r:
                return r.message, 404

    @ins.route("/trainers/<trainer_id>/batches")
    @ins.param('trainer_id', 'Trainer Unique Id', 'integer')
    @ins.doc(params={
        'year': {'in': 'query', 'description': '2021', 'type': 'integer'},
        'track': {'in': 'query', 'description': 'Python'}
    })
    class GetAllBatchesByQuery(Resource):
        @ins.marshal_with(batch_data, as_list=True, mask=None)
        def get(self, trainer_id):
            """Get all batches associated with the given trainer for the given year or trainingTrack"""
            year = request.args.get("year")
            track = request.args.get("track")
            if year is not None:
                try:
                    batches = BatchServices.get_all_batches_by_year(int(trainer_id), int(year))
                except ValueError:
                    return INVALID_ID_ERROR, 400  # Bad Request
                batches_as_json = convert_list_to_json(batches)
                return jsonify(batches_as_json)

            elif track is not None:
                try:
                    batches = BatchServices.search_for_batch(int(trainer_id), track)
                except ValueError:
                    return INVALID_ID_ERROR, 400  # Bad Request
                batches_as_json = convert_list_to_json(batches)
                return jsonify(batches_as_json)

            else:
                return "Please provide either track or year query parameters", 400
