from daos.note_dao import NoteDao
from models.note import Note
from services.note_service import NoteService

class NoteServiceImpl(NoteService):
    def __init__(self, note_dao: NoteDao):
        self.note_dao = note_dao

    def add_note(self, note: Note) -> Note:
        return self.note_dao.add_note(note)

    def get_single_note(self, note_id: int) -> Note:
        return self.note_dao.get_single_note(note_id)

    def get_all_notes(self) -> list[Note]:
        return self.note_dao.get_all_notes()

    def update_note(self, note: Note) -> Note:
        return self.note_dao.update_note(note)

    def delete_note(self, note_id: int) -> bool:
        return self.note_dao.delete_note(note_id)

    def get_all_notes_for_trainee(self, trainee_id: int) -> list[Note]:
        all_notes = self.note_dao.get_all_notes()
        to_return = []
        for note in all_notes:
            if note.trainee_id == trainee_id:
                to_return.append(note)
        return to_return

    def get_all_notes_for_trainee_for_week(self, trainee_id: int, week_number: int) -> list[Note]:
        all_notes = self.note_dao.get_all_notes()
        to_return = []
        for note in all_notes:
            if note.trainee_id == trainee_id and note.week_number == week_number:
                to_return.append(note)
        return to_return