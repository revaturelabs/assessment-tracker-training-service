from abc import ABC, abstractmethod

from models.note import Note

class NoteDao(ABC):
    @abstractmethod
    def add_note(self, note: Note) -> Note:
        pass

    @abstractmethod
    def get_single_note(self, note_id: int) -> Note:
        pass

    @abstractmethod
    def get_all_notes(self) -> list[Note]:
        pass

    @abstractmethod
    def update_note(self, updated: Note) -> Note:
        pass

    @abstractmethod
    def delete_note(self, note_id: int) -> bool:
        pass