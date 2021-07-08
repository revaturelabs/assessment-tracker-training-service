from abc import ABC, abstractmethod

from models.note import Note


class noteService(ABC):

    #Create
    @abstractmethod
    def add_note(self, note: Note) -> Note:
        pass

    #Read
    @abstractmethod
    def get_single_note(self, note_id: int) -> Note:
        pass
    @abstractmethod
    def get_all_notes(self) -> list[Note]:
        pass

    #Update
    @abstractmethod
    def update_note(self, note: Note) -> Note:
        pass

    #Delete
    @abstractmethod
    def delete_note(self, note_id: int) -> bool:
        pass


    #Business Logic
    @abstractmethod
    def get_all_notes_for_trainee(self, trainee_id: int) -> list[Note]:
        pass
    @abstractmethod
    def gat_all_notes_for_trainee_for_week(self, trainee_id: int, week_number: int) -> list[Note]:
        pass