from daos.daos_impl.batch_dao_impl import BatchDAOImpl
from daos.daos_impl.trainer_dao_impl import TrainerDAOImpl
from models.trainer import Trainer
from utils.connection import Connection

conn = Connection().conn


class TrainerService:

    trainer_dao = TrainerDAOImpl()
    batch_dao = BatchDAOImpl()

    @classmethod
    def login(cls, email):
        with conn:
            with conn.cursor() as cursor:
                return TrainerDAOImpl().login(cursor, email)

    @classmethod
    def get_trainer_by_id(cls, trainer_id):
        with conn:
            with conn.cursor() as cursor:
                return cls.trainer_dao.get_trainer_by_id(cursor, trainer_id)

    @classmethod
    def get_trainers_in_batch(cls, batch_id):
        with conn:
            with conn.cursor() as cursor:
                return cls.trainer_dao.get_trainers_in_batch(cursor, batch_id)

    @classmethod
    def get_years_for_trainer(cls, trainer_id):
        with conn:
            with conn.cursor() as cursor:
                years = TrainerDAOImpl().get_years_for_trainer(
                    cursor, trainer_id)
                years_dict = []
                for year in years:
                    years_dict.append({"year": year})
                return years_dict

    @classmethod
    def create_trainer(cls, trainer: Trainer):
        with conn:
            with conn.cursor() as cursor:
                return cls.trainer_dao.create_trainer(cursor, trainer)

    @classmethod
    def assign_trainer_to_batch(cls, trainer: Trainer, batch_id: int):
        with conn:
            with conn.cursor() as cursor:
                batch = cls.batch_dao.get_batch_by_id(cursor, batch_id)
                cls.trainer_dao.create_trainer_batch(cursor, trainer, batch)
                return trainer
