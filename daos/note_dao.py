from abc import ABC, abstractmethod
from typing import List

from models.note import Note


class NoteDao(ABC):
    @abstractmethod
    def add_note(self, cursor, note: Note) -> Note:
        pass

    @abstractmethod
    def get_single_note(self, cursor, note_id: int) -> Note:
        pass

    @abstractmethod
    def get_all_notes(self, cursor) -> List[Note]:
        pass

    @abstractmethod
    def update_note(self, cursor, updated: Note) -> Note:
        pass

    @abstractmethod
    def delete_note(self, cursor, note_id: int) -> bool:
        pass
