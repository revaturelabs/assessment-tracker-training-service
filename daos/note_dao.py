from abc import ABC, abstractmethod

from models.note import Note


class NoteDao(ABC):
    @staticmethod
    @abstractmethod
    def add_note(self, cursor, note: Note) -> Note:
        pass

    @staticmethod
    @abstractmethod
    def get_single_note(self, cursor, note_id: int) -> Note:
        pass

    @staticmethod
    @abstractmethod
    def get_all_notes(self, cursor) -> list[Note]:
        pass

    @staticmethod
    @abstractmethod
    def update_note(self, cursor, updated: Note) -> Note:
        pass

    @staticmethod
    @abstractmethod
    def delete_note(self, cursor, note_id: int) -> bool:
        pass
