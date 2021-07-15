import json
from models.associate import Associate
from flask import request, jsonify
from flask_restx import Api, Resource, fields

from exceptions.resource_not_found import ResourceNotFound
from services.associate_services import AssociateServices
from utils.json_tool import convert_list_to_json

INVALID_ID_ERROR = "Not a valid ID or No such batch exist with this ID"


def route(api):
    instructor = api.namespace(
        "instructors",
        description=
        "Instructors run batches. They must be able to access their batch information.",
        path="/")
    admin = api.namespace(
        "admin",
        description=
        "Administrators manage other users. They can create associates, trainers, and batches.",
        path="/")

    associate = api.model(
        "associate", {
            "firstName": fields.String(default="Zachary"),
            "lastName": fields.String(default="Vander Velden"),
            "trainingStatus": fields.String(default="Passed"),
            "id": fields.Integer(default=1),
            "email": fields.String(default="zvv@revature.com")
        })

    @admin.route("/associates")
    class GetAllAssociates(Resource):

        @admin.doc(summary="Get all associates.")
        def get(self):
            results = AssociateServices.get_all_associates()
            return jsonify([result.json() for result in results])

    @instructor.route("/associates/<int:associate_id>")
    @instructor.param("associate_id", "The associate's id number.")
    class GetAssociateId(Resource):

        @instructor.doc(summary="Get a specific Associate by their ID",
                        description="Get a specific Associate by their ID")
        @instructor.marshal_with(associate, mask=None)
        def get(self, associate_id):
            """Get a specific Associate by their ID"""
            try:
                batch = AssociateServices.get_associated_by_id(
                    int(associate_id))
                return jsonify(batch.json()), 200
            except ValueError:
                return INVALID_ID_ERROR, 400  # Bad Request
            except ResourceNotFound as r:
                return r.message, 404

    # @app.route("/associates/<associate_id>/batches/<batch_id>", methods=['GET'])
    # def get_associate_in_batch(associate_id, batch_id):
    #     """Get a specific Associate in the batch by their ID and a batch ID"""
    #     try:
    #         batch = AssociateServices.get_associate_in_batch(
    #             int(batch_id), int(associate_id))
    #         return jsonify(batch.json()), 200
    #     except ValueError:
    #         return INVALID_ID_ERROR, 400  # Bad Request
    #     except ResourceNotFound as r:
    #         return r.message, 404

    # @app.route("/batches/<batch_id>/associates", methods=['GET'])
    # def get_all_associates_in_batch(batch_id):
    #     """Get all Associates in a batch by the batch ID"""
    #     try:
    #         batch = AssociateServices.get_all_associates_in_batch(int(batch_id))
    #         batches_as_json = convert_list_to_json(batch)
    #         return jsonify(batches_as_json), 200
    #     except ValueError:
    #         return INVALID_ID_ERROR, 400  # Bad Request
    #     except ResourceNotFound as r:
    #         return r.message, 404

    # @app.route("/associates", methods=["POST"])
    # def post_associate():
    #     """Create a new associate.

    #     Accepts a JSON input:
    #     {
    #         "firstName": str,
    #         "lastName": str,
    #         "email": str,
    #         "trainingStatus": str,
    #     }
    #     """
    #     try:
    #         body = json.loads(request.data.decode("utf-8"))
    #         associate = Associate(body["firstName"], body["lastName"],
    #                               body["email"], body["trainingStatus"])
    #         associate = AssociateServices.create_new_associate(associate)
    #         return jsonify(associate.json()), 201
    #     except ValueError:
    #         return INVALID_ID_ERROR, 400  # Bad Request
    #     except ResourceNotFound as r:
    #         return r.message, 404

    # @app.route("/associates/register", methods=["POST"])
    # def post_associate_batch():
    #     """
    #     Create a new associate-batch join relationship

    #     Accepts a JSON input:
    #     {
    #         "associateId": int,
    #         "batchId": int
    #     }
    #     """
    #     try:
    #         body = request.json
    #         new_registration = AssociateServices.create_assoicate_batch_join(
    #             int(body["associateId"]), int(body["batchId"]))
    #         result = {"result": new_registration}
    #         return jsonify(result), 201
    #     except (ValueError):
    #         return INVALID_ID_ERROR, 400
    #     except (KeyError, TypeError):
    #         return "Invalid JSON body", 400
    #     except ResourceNotFound as r:
    #         return r.message, 404
