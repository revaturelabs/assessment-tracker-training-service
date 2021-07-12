from typing import List

from daos.note_dao import NoteDao
from models.note import Note
from services.note_service import NoteService
from utils.connection import Connection

conn = Connection().conn


class NoteServiceImpl(NoteService):

    def __init__(self, note_dao: NoteDao):
        self.note_dao = note_dao

    def add_note(self, note: Note) -> Note:
        with conn:
            with conn.cursor() as cursor:
                return self.note_dao.add_note(cursor, note)

    def get_single_note(self, note_id: int) -> Note:
        with conn:
            with conn.cursor() as cursor:
                return self.note_dao.get_single_note(cursor, note_id)

    def get_all_notes(self) -> List[Note]:
        with conn:
            with conn.cursor() as cursor:
                return self.note_dao.get_all_notes(cursor)

    def update_note(self, note: Note) -> Note:
        with conn:
            with conn.cursor() as cursor:
                return self.note_dao.update_note(cursor, note)

    def delete_note(self, note_id: int) -> bool:
        with conn:
            with conn.cursor() as cursor:
                return self.note_dao.delete_note(cursor, note_id)

    def get_all_notes_for_trainee(self, associate_id: int) -> List[Note]:
        with conn:
            with conn.cursor() as cursor:
                all_notes = self.note_dao.get_all_notes(cursor)
                to_return = []
                for note in all_notes:
                    if note.associate_id == associate_id:
                        to_return.append(note)
                return to_return

    def get_all_notes_for_trainee_for_week(self, associate_id: int,
                                           week_number: int) -> List[Note]:
        with conn:
            with conn.cursor() as cursor:
                all_notes = self.note_dao.get_all_notes(cursor)
                to_return = []
                for note in all_notes:
                    if note.associate_id == associate_id and note.week_number == week_number:
                        to_return.append(note)
                return to_return
