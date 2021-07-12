from abc import ABC, abstractmethod
from typing import List

from models.note import Note


class NoteService(ABC):

    # Create
    @abstractmethod
    def add_note(self, note: Note) -> Note:
        pass

    # Read
    @abstractmethod
    def get_single_note(self, note_id: int) -> Note:
        pass

    @abstractmethod
    def get_all_notes(self) -> List[Note]:
        pass

    # Update
    @abstractmethod
    def update_note(self, note: Note) -> Note:
        pass

    # Delete
    @abstractmethod
    def delete_note(self, note_id: int) -> bool:
        pass

    # Business Logic
    @abstractmethod
    def get_all_notes_for_trainee(self, associate_id: int) -> List[Note]:
        pass

    @abstractmethod
    def get_all_notes_for_trainee_for_week(self, associate_id: int,
                                           week_number: int) -> List[Note]:
        pass
