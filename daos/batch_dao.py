from abc import abstractmethod, ABC
from typing import List

from models.batch import Batch


class BatchDAO(ABC):

    @staticmethod
    @abstractmethod
    def create_batch(cursor, batch:Batch) -> Batch:
        pass

    @staticmethod
    @abstractmethod
    def get_all_batches_by_year(cursor, trainer_id: int, year: int) -> List[Batch]:
        pass

    @staticmethod
    @abstractmethod
    def get_batch_by_id(cursor, batch_id: int) -> Batch:
        pass

    @abstractmethod
    def search_for_batch(self, trainer_id, track):
        pass
