from typing import List

import psycopg2

from daos.note_dao import NoteDao
from exceptions.resource_not_found import ResourceNotFound
from models.note import Note


class NoteDAOImpl(NoteDao):

    @staticmethod
    def add_note(cursor, note: Note) -> Note:
        if note.week_number < 0:
            raise ValueError()
        try:
            """Creates a note for an Associate on a given week for a Batch"""
            sql = "insert into notes (batch_id, cont, associate_id, week_number) values(%s, %s, %s, %s) returning id"
            cursor.execute(sql, (note.batch_id, note.content, note.associate_id,
                                 note.week_number))
            n_id = cursor.fetchone()[0]
            note.note_id = n_id
            return note
        except psycopg2.Error as e:
            if int(e.pgcode) == 23503 or int(e.pgcode) == 42830:
                raise ResourceNotFound("The foreign keys provided do not exist")

    @staticmethod
    def get_single_note(cursor, note_id: int) -> Note:
        """Takes in an id for a note record and returns a Note object"""
        sql = "select * from notes where id = %s"
        cursor.execute(sql, [note_id])
        records = cursor.fetchall()
        if records:
            record = records[0]
            note = Note(note_id=record[0],
                        batch_id=record[1],
                        content=record[2],
                        associate_id=record[3],
                        week_number=record[4])
            return note
        else:
            raise ResourceNotFound("No note could be found with the given id")

    @staticmethod
    def get_all_notes(cursor) -> List[Note]:
        """Returns all the notes"""
        sql = "select * from notes"
        cursor.execute(sql)
        records = cursor.fetchall()
        notes = []
        for note in records:
            notes.append(
                Note(note_id=note[0],
                     batch_id=note[1],
                     content=note[2],
                     associate_id=note[3],
                     week_number=note[4]))
        return notes

    @staticmethod
    def update_note(cursor, updated: Note) -> Note:
        """Updates note"""
        if updated.week_number < 0:
            raise ValueError()
        try:
            sql = "update notes set batch_id = %s, cont = %s, associate_id = %s, week_number = %s where id = %s returning id"
            cursor.execute(
                sql, (updated.batch_id, updated.content, updated.associate_id,
                      updated.week_number, updated.note_id))
            n_id = cursor.fetchone()
            if n_id is not None:
                return updated
            else:
                raise ResourceNotFound("Note could not be found")
        except psycopg2.Error as e:
            if int(e.pgcode) == 23503 or int(e.pgcode) == 42830:
                raise ResourceNotFound("The foreign keys provided do not exist")

    @staticmethod
    def delete_note(cursor, note_id: int) -> bool:
        """Deletes a note and returns True if successful"""
        sql = "delete from notes where id = %s returning id"
        cursor.execute(sql, [note_id])
        n_id = cursor.fetchone()
        if n_id is not None:
            return True
        else:
            raise ResourceNotFound("No note could be found with the given id")
