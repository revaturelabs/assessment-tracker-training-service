from flask import request
from flask_restx import Resource, fields

from daos.daos_impl.note_dao_impl import NoteDAOImpl
from daos.note_dao import NoteDao
from exceptions.resource_not_found import ResourceNotFound
from models.note import Note
from services.note_service import NoteService
from services.note_service_impl import NoteServiceImpl

INVALID_ID_ERROR = "Not a valid ID or No such batch exist with this ID"


def route(ins):
    note_dao: NoteDao = NoteDAOImpl()
    note_service: NoteService = NoteServiceImpl(note_dao)

    note_data = ins.model('Note Data', {
        "id": fields.Integer,
        "batchId": fields.Integer,
        "cont": fields.String,
        "associateId": fields.Integer,
        "weekNumber": fields.Integer
    })

    # Create a note
    @ins.route("/notes")
    class UnparamterizedNotes(Resource):
        @ins.expect(note_data)
        @ins.marshal_with(note_data, mask=None)
        @ins.response(201, 'Created')
        @ins.response(422, 'Unprocessable Entity')
        def post(self):
            """Creates a new note"""
            try:
                body = request.json
                note = Note.json_parse(body)
                fresh_note = note_service.add_note(note)
                return fresh_note.json(), 201
            except ValueError:
                # This error might be thrown if the week number is invalid
                return "Invalid week number provided", 422
            except ResourceNotFound as r:
                # This error might be thrown if their is no such batch or trainee
                return r.message, 422

        @ins.marshal_with(note_data, as_list=True, mask=None)
        @ins.response(200, 'OK')
        def get(self):
            """ Gets all notes"""
            notes = note_service.get_all_notes()
            json_notes = [note.json() for note in notes]
            return json_notes, 200

    @ins.route("/notes/<int:note_id>")
    @ins.param('note_id', 'Note Unique Id', fields.Integer)
    @ins.response(200, 'OK')
    class ParamterizedNotes(Resource):

        @ins.marshal_with(note_data, mask=None)
        @ins.response(404, 'Resource not Found')
        def get(self, note_id):
            """ Gets a specific note by ID """
            try:
                note = note_service.get_single_note(int(note_id))
                return note.json(), 200
            except ResourceNotFound as r:
                # invalid note id
                return r.message, 404

        @ins.expect(note_data)
        @ins.marshal_with(note_data, mask=None)
        @ins.response(200, 'OK')
        @ins.response(404, 'Resource not Found')
        @ins.response(422, 'Unprocessable Entity')
        def put(self, note_id):
            """Updates a note by ID"""
            try:
                body = request.json
                note = Note.json_parse(body)
                note.note_id = int(note_id)
                note_service.update_note(note)
                return note.json()
            except ValueError:
                # tried to update the note with bad values such as week number
                return "Invalid week number", 422
            except ResourceNotFound as r:
                # couldn't find the note or updated the note with bad trainee or batch ids
                return r.message, 404

        @ins.response(200, 'OK')
        @ins.response(404, 'Resource not Found')
        def delete(self, note_id):
            """Deletes a note by ID"""
            try:
                note_service.delete_note(int(note_id))
                return "Deleted Successfully", 200
            except ResourceNotFound as r:
                # note id is invalid
                return r.message, 404

    @ins.route("/associates/<int:associate_id>/notes")
    @ins.param('associate_id', 'Associate Unique Id')
    class GetNotesForAssociate(Resource):
        @ins.marshal_with(note_data, as_list=True, mask=None)
        @ins.response(200, 'OK')
        @ins.response(404, 'Resource not Found')
        def get(self, associate_id):
            week = request.args.get("week")
            try:
                if week is not None:
                    notes = note_service.get_all_notes_for_trainee_for_week(int(associate_id), int(week))
                else:
                    notes = note_service.get_all_notes_for_trainee(int(associate_id))
                json_notes = [note.json() for note in notes]
                return json_notes, 200
            except ResourceNotFound as r:
                # Bad trainee id passed
                return r.message, 404
