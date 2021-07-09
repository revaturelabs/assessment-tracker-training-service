from abc import ABC, abstractmethod
from models.trainer import Trainer
from models.batch import Batch


class TrainerDAO(ABC):
    @staticmethod
    @abstractmethod
    def get_trainer_by_id(self, trainer_id):
        pass

    @staticmethod
    @abstractmethod
    def get_trainers_in_batch(self, batch_id):
        pass

    @staticmethod
    @abstractmethod
    def login(self, email):
        pass

    @staticmethod
    @abstractmethod
    def get_years_for_trainer(self, trainer_id):
        pass

    @staticmethod
    @abstractmethod
    def create_trainer(cursor, trainer: Trainer) -> Trainer:
        pass

    @staticmethod
    @abstractmethod
    def create_trainer_batch(cursor, trainer: Trainer, batch: Batch) -> bool:
        pass
