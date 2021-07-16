from abc import abstractmethod, ABC
from typing import List
from models.batch import Batch
from models.associate import Associate


class AssociateDAO(ABC):

    @staticmethod
    @abstractmethod
    def get_associate_by_id(cursor, associate_id):
        pass

    @staticmethod
    @abstractmethod
    def get_all_associates(cursor):
        pass

    @staticmethod
    @abstractmethod
    def get_associate_in_batch(cursor, associate_id, batch_id):
        pass

    @staticmethod
    @abstractmethod
    def create_associate(cursor, associate: Associate) -> Associate:
        pass

    @staticmethod
    @abstractmethod
    def get_all_associates_in_batch(self, batch_id):
        pass

    @staticmethod
    @abstractmethod
    def create_associate_batch(cursor, associate: Associate,
                               batch: Batch) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def batch_create_associate_batch(cursor, associate_ids: List[int],
                                     batch: Batch,
                                     training_status: str) -> bool:
        pass
