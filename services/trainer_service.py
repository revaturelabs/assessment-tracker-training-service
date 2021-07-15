from daos.daos_impl.trainer_dao_impl import TrainerDAOImpl
from utils.connection import Connection

conn = Connection().conn


class TrainerService:

    trainer_dao = TrainerDAOImpl()

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
    def get_all_trainers(cls):
        with conn:
            with conn.cursor() as cursor:
                trainers = TrainerDAOImpl().get_all_trainers(cursor)
                trainers_list = [trainer.json() for trainer in trainers]
                return trainers_list

