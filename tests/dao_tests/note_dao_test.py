import unittest

from daos.daos_impl.note_dao_impl import NoteDAOImpl
from exceptions.resource_not_found import ResourceNotFound
from models.note import Note
from utils.connection import Connection

conn = Connection().conn

note_dao = NoteDAOImpl()

test_note = Note(0, 1, 1, 1, "Test Note")


class NoteDAOTest(unittest.TestCase):

    def test_create_note(self):
        with conn:
            with conn.cursor() as cursor:
                note_dao.add_note(cursor, test_note)
                assert test_note.note_id != 0
            conn.rollback()

    def test_get_single_note(self):
        with conn:
            with conn.cursor() as cursor:
                note_dao.add_note(cursor, test_note)
                assert note_dao.get_single_note(cursor, test_note.note_id)
            conn.rollback()

    def test_get_single_note_fail(self):
        with conn:
            with conn.cursor() as cursor:
                try:
                    note_dao.get_single_note(cursor, 200)
                except ResourceNotFound:
                    assert True
            conn.rollback()

    def test_get_all_notes(self):
        with conn:
            with conn.cursor() as cursor:
                assert note_dao.get_all_notes(cursor)
            conn.rollback()

    def test_update_note(self):
        with conn:
            with conn.cursor() as cursor:
                test_note.content = 'Updated content'
                note = note_dao.update_note(cursor, test_note)
                assert note.content == test_note.content
            conn.rollback()

    def test_update_note_fail(self):
        with conn:
            with conn.cursor() as cursor:
                try:
                    test_note.note_id = 200
                    note_dao.update_note(cursor, test_note)
                except ResourceNotFound:
                    assert True
            conn.rollback()

    def test_delete_note(self):
        with conn:
            with conn.cursor() as cursor:
                assert note_dao.delete_note(cursor, test_note.note_id)
            conn.rollback()

    def test_delete_note_fail(self):
        with conn:
            with conn.cursor() as cursor:
                try:
                    test_note.note_id = 200
                    note_dao.delete_note(cursor, test_note.note_id)
                except ResourceNotFound:
                    assert True
            conn.rollback()
