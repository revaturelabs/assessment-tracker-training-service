import json
from models.associate import Associate
from flask import request
from flask_restx import Resource, fields

from exceptions.resource_not_found import ResourceNotFound
from services.associate_services import AssociateServices
from utils.json_tool import convert_list_to_json

INVALID_ID_ERROR = "Not a valid ID or No such batch exist with this ID"


def route(ans, ins):
    associate = ins.model(
        "associate", {
            "firstName": fields.String(default="Zachary"),
            "lastName": fields.String(default="Vander Velden"),
            "trainingStatus": fields.String(default="Passed"),
            "id": fields.Integer(default=1),
            "email": fields.String(default="zvv@revature.com")
        })

    @ans.route("/associates")
    class GetAllAssociates(Resource):
        new_associate = ans.model(
            "new_associate", {
                "firstName": fields.String,
                "lastName": fields.String,
                "email": fields.String,
                "trainingStatus": fields.String
            })

        def get(self):
            """Get all associates"""
            results = AssociateServices.get_all_associates()
            return [result.json() for result in results]

        @ans.expect(new_associate)
        def post(self):
            """Create a new associate."""
            try:
                body = json.loads(request.data.decode("utf-8"))
                associate = Associate(body["firstName"], body["lastName"],
                                      body["email"], body["trainingStatus"])
                associate = AssociateServices.create_new_associate(associate)
                return associate.json(), 201
            except ValueError:
                return INVALID_ID_ERROR, 400  # Bad Request
            except ResourceNotFound as r:
                return r.message, 404

    @ins.route("/associates/<int:associate_id>")
    @ins.param("associate_id", "The associate's id number.")
    @ins.response(404, "No associate could be found with that id and/or batch")
    @ins.response(400, "Not a valid ID or No such batch exist with this ID")
    class GetAssociateId(Resource):

        @ins.doc(summary="Get a specific Associate by their ID",
                 description="Get a specific Associate by their ID")
        @ins.marshal_with(associate, mask=None)
        def get(self, associate_id):
            """Get a specific Associate by their ID"""
            try:
                batch = AssociateServices.get_associated_by_id(
                    int(associate_id))
                return batch.json(), 200
            except ValueError:
                return INVALID_ID_ERROR, 400  # Bad Request
            except ResourceNotFound as r:
                return r.message, 404

    @ins.route("/associates/<int:associate_id>/batches/<int:batch_id>")
    @ins.param("associate_id", "The associate's id number.")
    @ins.param("batch_id", "The batch's id number.")
    @ins.response(404, "No associate could be found with that id and/or batch")
    @ins.response(400, "Not a valid ID or No such batch exist with this ID")
    class GetAssociateInBatch(Resource):

        @ins.doc(
            summary="Get an associate by associate and batch id.",
            description=
            "Get a specific Associate in the batch by their ID and a batch ID.")
        @ins.marshal_with(associate, mask=None)
        def get(self, associate_id, batch_id):
            """Get a specific Associate in the batch by their ID and a batch ID"""
            try:
                batch = AssociateServices.get_associate_in_batch(
                    int(batch_id), int(associate_id))
                return batch.json(), 200
            except ValueError:
                return INVALID_ID_ERROR, 400  # Bad Request
            except ResourceNotFound as r:
                return r.message, 404

    @ins.route("/batches/<int:batch_id>/associates")
    @ins.param("batch_id", "The batch's id number.")
    class GetAllAssociatesInBatch(Resource):

        @ins.doc(summary="Get all Associates in a batch by the batch ID",
                 description="Get all Associates in a batch by the batch ID")
        @ins.marshal_with(associate, mask=None, as_list=True)
        def get(self, batch_id):
            """Get all Associates in a batch by the batch ID"""
            try:
                batch = AssociateServices.get_all_associates_in_batch(
                    int(batch_id))
                batches_as_json = convert_list_to_json(batch)
                return batches_as_json, 200
            except ValueError:
                return INVALID_ID_ERROR, 400  # Bad Request
            except ResourceNotFound as r:
                return r.message, 404

    @ans.route("/associates/register")
    class PostAssociateBatch(Resource):
        associate_batch = ans.model("associate_batch", {
            "associateId": fields.Integer,
            "batchId": fields.Integer
        })

        @ans.doc(summary="Register an associate into a batch.",
                 description="Creates a new associate-batch join relationship.")
        @ans.expect(associate_batch)
        def post(self):
            """Create a new associate-batch join relationship"""
            try:
                body = request.json
                new_registration = AssociateServices.create_assoicate_batch_join(
                    int(body["associateId"]), int(body["batchId"]))
                result = {"result": new_registration}
                return result, 201
            except (ValueError):
                return INVALID_ID_ERROR, 400
            except (KeyError, TypeError):
                return "Invalid JSON body", 400
            except ResourceNotFound as r:
                return r.message, 404
