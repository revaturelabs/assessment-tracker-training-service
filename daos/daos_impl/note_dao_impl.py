from daos.note_dao import NoteDao
from exceptions.resource_not_found import ResourceNotFound
from models.note import Note
from utils.connection import Connection

conn = Connection.conn


class NoteDAOImpl(NoteDao):
    def add_note(self, cursor, note: Note) -> Note:
        """Creates a note for an Associate on a given week for a Batch"""
        sql = """insert into note (default, %s, %s, %s, %s) returning book_id"""
        cursor.execute(sql, (note.batch_id, note.content, note.trainee_id, note.week_number))
        conn.commit()
        n_id = cursor.fetchone()[0]
        note.note_id = n_id
        return note

    def get_single_note(self, cursor, note_id: int) -> Note:
        """Takes in an id for a note record and returns a Note object"""
        sql = """select * from note where note_id = %s"""
        cursor.execute(sql, [note_id])
        records = cursor.fetchall()
        if records:
            record = records[0]
            note = Note(note_id=record[0],
                        batch_id=record[1],
                        content=record[2],
                        trainee_id=record[3],
                        week_number=record[4])
            return note
        else:
            raise ResourceNotFound("No note could be found with the given id")

    def get_all_notes(self, cursor) -> list[Note]:
        """Returns all the notes"""
        sql = """select * from note"""
        cursor.execute(sql)
        records = cursor.fetchall()
        notes = []
        for note in records:
            notes.append(Note(note_id=note[0],
                              batch_id=note[1],
                              content=note[2],
                              trainee_id=note[3],
                              week_number=note[4]))
        return notes

    def update_note(self, cursor, updated: Note) -> Note:
        """Updates the note's content"""
        sql = """update note set content = %s where note_id = % returning note_id"""
        cursor.execute(sql, (updated.content, updated.note_id))
        conn.commit()
        n_id = cursor.fetchone()
        if n_id is not None:
            return updated
        else:
            raise ResourceNotFound("Note could not be found")

    def delete_note(self, cursor, note_id: int) -> bool:
        """Deletes a note and returns True if successful"""
        sql = """delete from note where note_id = %s returning note_id"""
        cursor.execute(sql, [note_id])
        conn.commit()
        n_id = cursor.fetchone()
        if n_id is not None:
            return True
        else:
            raise ResourceNotFound("No note could be found with the given id")