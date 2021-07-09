from flask import jsonify, request

from daos.daos_impl.note_dao_impl import NoteDAOImpl
from daos.note_dao import NoteDao
from exceptions.resource_not_found import ResourceNotFound
from models.note import Note
from services.note_service import NoteService
from services.note_service_impl import NoteServiceImpl

INVALID_ID_ERROR = "Not a valid ID or No such batch exist with this ID"


def route(app):

    note_dao: NoteDao = NoteDAOImpl()
    note_service: NoteService = NoteServiceImpl(note_dao)

    # Create a note
    @app.route("/note", methods=['POST'])
    def new_note():
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

    # Get a note
    @app.route("/note/<note_id>", methods=['GET'])
    def get_note_id(note_id):
        try:
            note = note_service.get_single_note(int(note_id))
            return jsonify(note.json()), 200
        except ResourceNotFound as r:
            # invalid note id
            return r.message, 404

    # Get all notes
    @app.route("/note", methods=['GET'])
    def get_notes_all():
        try:
            trainee = request.args.get("traineeId")
            week = request.args.get("week")
            if trainee is not None and week is None:
                # if you pass the trainee id in the request
                notes = note_service.get_all_notes_for_trainee(int(trainee))
            elif week is not None and trainee is not None:
                # if you pass the week number in the request
                if int(week) > 12:
                    raise ValueError()
                notes = note_service.get_all_notes_for_trainee_for_week(int(trainee), int(week))
            else:
                # if you don't pass anything
                notes = note_service.get_all_notes()
            json_notes = [note.json() for note in notes]
            return jsonify(json_notes), 200
        except ValueError:
            # Bad week number passed
            return "Invalid week number", 422
        except ResourceNotFound as r:
            # Bad trainee id passed
            return r.message, 404

    # update a note
    @app.route("/note/<note_id>", methods=['PUT'])
    def update_note(note_id):
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

    # Delete a note
    @app.route("/note/<note_id>", methods=['DELETE'])
    def delete_note(note_id):
        try:
            note_service.delete_note(int(note_id))
            return "Deleted Successfully", 200
        except ResourceNotFound as r:
            # note id is invalid
            return r.message, 404

