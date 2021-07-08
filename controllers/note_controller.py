from flask import jsonify, request

from exceptions.resource_not_found import ResourceNotFound
from models.note import Note
from services.note_service import NoteService

INVALID_ID_ERROR = "Not a valid ID or No such batch exist with this ID"


def route(app):

    note_service: NoteService = None;

    # Create a note
    @app.route("/note", methods=['POST'])
    def new_note(note: Note):
        try:
            fresh_note = note_service.add_note(note);
            return fresh_note, 201
        except ValueError:
            return INVALID_ID_ERROR, 422

    # Get a note
    @app.route("/note/<note_id>", methods=['GET'])
    def get_note_id(note_id):
        try:
            note = note_service.get_single_note(int(note_id))
            return jsonify(note.json()), 200
        except ResourceNotFound as r:
            return r.message, 404

    # Get all notes
    @app.route("/note", methods=['GET'])
    def get_notes_all():
        try:
            trainee = request.args.get("traineeId")
            week = request.args.get("week")
            if trainee is not None:
                notes = note_service.get_all_notes_for_trainee(int(trainee))
            elif week is not None:
                notes = note_service.get_all_notes_for_trainee_for_week()
            else:
                notes = note_service.get_all_notes()
            json_notes = [note.json() for note in notes]
            return jsonify(json_notes), 200
        except ValueError:
            return "Invalid week number", 400
        except ResourceNotFound as r:
            return r.message, 404

    # update a note
    @app.route("/note/<note_id>", methods=['PUT'])
    def update_note(note_id):
        try:
            note = note_service.get_single_note(int(note_id))
            note.note_id = int(note_id)
            note_service.update_note(note)
            return note
        except ValueError:
            return INVALID_ID_ERROR, 400
        except ResourceNotFound as r:
            return r.message, 404

    # Delete a note
    @app.route("/note/<note_id>", methods=['DELETE'])
    def delete_note(note_id):
        try:
            note_service.delete_note(int(note_id))
            return True
        except ResourceNotFound as r:
            return r.message, 404

