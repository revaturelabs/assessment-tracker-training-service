from copy import copy
from daos.daos_impl.associate_dao_impl import AssociateDAOImpl as a
from daos.daos_impl.batch_dao_impl import BatchDAOImpl as b
from daos.daos_impl.note_dao_impl import NoteDAOImpl as n
from exceptions.resource_not_found import ResourceNotFound
from models.associate import Associate
from models.batch import Batch
from models.note import Note
from pytest import raises
from utils.connection import Connection

conn = Connection().conn

ASSOCIATE = Associate("Testy", "McTesterson", "test@test.test", "")
BATCH = Batch("TestBatch", "Python Automation", 1625788800, 1631145600)
TEST_NOTE = Note(0, 1, 1, 1, "Test Note")


def test_create_note():
    with conn:
        with conn.cursor() as cursor:
            associate = copy(ASSOCIATE)
            batch = copy(BATCH)
            associate.id = a.create_associate(cursor, associate).id
            batch.id = b.create_batch(cursor, batch).id
            test_note = Note(0, batch.id, associate.id, 1, "Test Note")
            test_note.note_id = n.add_note(cursor, test_note).note_id
            assert test_note.note_id != 0
        conn.rollback()


def test_get_single_note():
    with conn:
        with conn.cursor() as cursor:
            associate = copy(ASSOCIATE)
            batch = copy(BATCH)
            associate.id = a.create_associate(cursor, associate).id
            batch.id = b.create_batch(cursor, batch).id
            test_note = Note(0, batch.id, associate.id, 1, "Test Note")
            test_note.note_id = n.add_note(cursor, test_note).note_id
            assert n.get_single_note(cursor, test_note.note_id)
        conn.rollback()


def test_get_single_note_fail():
    with conn:
        with conn.cursor() as cursor:
            associate = copy(ASSOCIATE)
            batch = copy(BATCH)
            associate.id = a.create_associate(cursor, associate).id
            batch.id = b.create_batch(cursor, batch).id
            test_note = Note(0, batch.id, associate.id, 1, "Test Note")
            test_note.note_id = n.add_note(cursor, test_note).note_id
            with raises(ResourceNotFound):
                n.get_single_note(cursor, 200)
        conn.rollback()


def test_get_all_notes():
    with conn:
        with conn.cursor() as cursor:
            associate = copy(ASSOCIATE)
            batch = copy(BATCH)
            associate.id = a.create_associate(cursor, associate).id
            batch.id = b.create_batch(cursor, batch).id
            test_note = Note(0, batch.id, associate.id, 1, "Test Note")
            test_note.note_id = n.add_note(cursor, test_note).note_id
            notes = n.get_all_notes(cursor)
            assert len(notes) != 0
        conn.rollback()


def test_update_note():
    with conn:
        with conn.cursor() as cursor:
            associate = copy(ASSOCIATE)
            batch = copy(BATCH)
            associate.id = a.create_associate(cursor, associate).id
            batch.id = b.create_batch(cursor, batch).id
            test_note = Note(0, batch.id, associate.id, 1, "Test Note")
            test_note.note_id = n.add_note(cursor, test_note).note_id
            upd_note = n.get_single_note(cursor, test_note.note_id)
            upd_note.content = 'Updated content'
            note = n.update_note(cursor, upd_note)
            assert note.content == upd_note.content
        conn.rollback()


def test_update_note_fail():
    with conn:
        with conn.cursor() as cursor:
            with raises(ResourceNotFound):
                test_note = copy(TEST_NOTE)
                test_note.note_id = 0
                n.update_note(cursor, test_note)
        conn.rollback()


def test_delete_note():
    with conn:
        with conn.cursor() as cursor:
            associate = copy(ASSOCIATE)
            batch = copy(BATCH)
            associate.id = a.create_associate(cursor, associate).id
            batch.id = b.create_batch(cursor, batch).id
            test_note = Note(0, batch.id, associate.id, 1, "Test Note")
            test_note.note_id = n.add_note(cursor, test_note).note_id
            assert n.delete_note(cursor, test_note.note_id)
        conn.rollback()


def test_delete_note_fail():
    with conn:
        with conn.cursor() as cursor:
            with raises(ResourceNotFound):
                test_note = copy(TEST_NOTE)
                test_note.note_id = 0
                n.delete_note(cursor, test_note.note_id)
        conn.rollback()
