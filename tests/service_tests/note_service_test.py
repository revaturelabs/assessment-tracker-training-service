from unittest.mock import MagicMock

from daos.note_dao import NoteDao
from models.note import Note
from services.note_service import NoteService
from services.note_service_impl import NoteServiceImpl

note_dao: NoteDao = None

notes = [
    Note(1, 1, 1, 1, "Test Note"),
    Note(2, 1, 2, 1, "Test Note 2"),
    Note(3, 1, 3, 1, "Test Note 3"),
    Note(4, 1, 2, 2, "Test Note 4"),
    Note(5, 1, 3, 2, "Test Note 5"),
    Note(6, 1, 3, 3, "Test Note 6"),
    Note(7, 1, 3, 3, "Test Note 7")
]
note_dao.get_all_notes = MagicMock(return_value = notes)

note_service: NoteService = NoteServiceImpl(note_dao)

def test_1_get_all_notes_for_trainee():
    for i in range(1, 4):
        all_notes = note_service.get_all_notes_for_trainee(i)
        assert len(all_notes) == i

def test_1_get_all_empty_notes():
    all_notes = note_service.get_all_notes_for_trainee(0)
    assert len(all_notes) == 0
    all_notes = note_service.get_all_notes_for_trainee(4)
    assert len(all_notes) == 0

def test_2_get_all_notes_for_trainee_for_week():
    all_notes = note_service.get_all_notes_for_trainee_for_week(1, 1)
    assert len(all_notes) == 1
    all_notes = note_service.get_all_notes_for_trainee_for_week(2, 2)
    assert len(all_notes) == 1
    all_notes = note_service.get_all_notes_for_trainee_for_week(3, 3)
    assert len(all_notes) == 2

def test_2_get_invalid_notes():
    all_notes = note_service.get_all_notes_for_trainee_for_week(0, 2)
    assert len(all_notes) == 0
    all_notes = note_service.get_all_notes_for_trainee_for_week(1, 3)
    assert len(all_notes) == 0