from daos.daos_impl.batch_dao_impl import BatchDAOImpl
from models.batch import Batch
from utils.connection import Connection

conn = Connection().conn


class BatchServices:

    @classmethod
    def create_batch(cls, batch: Batch):
        with conn:
            with conn.cursor() as cursor:
                return BatchDAOImpl().create_batch(cursor, batch)

    @classmethod
    def get_batch_by_id(cls, batch_id):
        with conn:
            with conn.cursor() as cursor:
                return BatchDAOImpl().get_batch_by_id(cursor, batch_id)

    @classmethod
    def get_all_batches_by_year(cls, trainer_id, year):
        with conn:
            with conn.cursor() as cursor:
                return BatchDAOImpl().get_all_batches_by_year(
                    cursor, trainer_id, year)

    @classmethod
    def search_for_batch(cls, trainer_id, track):
        with conn:
            with conn.cursor() as cursor:
                return BatchDAOImpl().search_for_batch(cursor, trainer_id,
                                                       track)
