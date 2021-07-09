from abc import abstractmethod, ABC
from models.associate import Associate


class AssociateDAO(ABC):
    @staticmethod
    @abstractmethod
    def get_associate_by_id(cursor, associate_id):
        pass

    @staticmethod
    @abstractmethod
    def get_associate_in_batch(cursor, associate_id, batch_id):
        pass

    @staticmethod
    @abstractmethod
    def create_associate(cursor, associate: Associate) -> Associate:
        pass
