import json
from models.associate import Associate
from flask import request, jsonify

from exceptions.resource_not_found import ResourceNotFound
from services.associate_services import AssociateServices
from utils.json_tool import convert_list_to_json

INVALID_ID_ERROR = "Not a valid ID or No such batch exist with this ID"


def route(app):

    #Get all associates endpoint
    @app.get("/associates")
    def get_all_associates():
        results = AssociateServices.get_all_associates()
        return jsonify([result.json() for result in results])

    # Get associate by id endpoint
    @app.route("/associates/<associate_id>", methods=['GET'])
    def get_associate_id(associate_id):
        """Get a specific Associate by their ID"""
        try:
            batch = AssociateServices.get_associated_by_id(int(associate_id))
            return jsonify(batch.json()), 200
        except ValueError:
            return INVALID_ID_ERROR, 400  # Bad Request
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/associates/<associate_id>/batches/<batch_id>", methods=['GET'])
    def get_associate_in_batch(associate_id, batch_id):
        """Get a specific Associate in the batch by their ID and a batch ID"""
        try:
            batch = AssociateServices.get_associate_in_batch(
                int(batch_id), int(associate_id))
            return jsonify(batch.json()), 200
        except ValueError:
            return INVALID_ID_ERROR, 400  # Bad Request
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/batches/<batch_id>/associates", methods=['GET'])
    def get_all_associates_in_batch(batch_id):
        """Get all Associates in a batch by the batch ID"""
        try:
            batch = AssociateServices.get_all_associates_in_batch(int(batch_id))
            batches_as_json = convert_list_to_json(batch)
            return jsonify(batches_as_json), 200
        except ValueError:
            return INVALID_ID_ERROR, 400  # Bad Request
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/associates", methods=["POST"])
    def post_associate_in_batch():
        """Create a new associate in a specified branch.

        Accepts a JSON input:
        {
            "firstName": str,
            "lastName": str,
            "email": str,
            "trainingStatus": str,
            "batchId": int
        }
        """
        try:
            body = json.loads(request.data.decode("utf-8"))
            associate = Associate(body["firstName"], body["lastName"],
                                  body["email"], body["trainingStatus"])
            associate.id = AssociateServices.create_associate_in_batch(
                associate, body["batchId"]).id
            return jsonify(associate.json()), 201
        except ValueError:
            return INVALID_ID_ERROR, 400  # Bad Request
        except ResourceNotFound as r:
            return r.message, 404
