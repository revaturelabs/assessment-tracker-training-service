from datetime import datetime
from math import floor
from models.batch import Batch

from daos.trainer_dao import TrainerDAO
from exceptions.resource_not_found import ResourceNotFound
from models.trainer import Trainer


class TrainerDAOImpl(TrainerDAO):

    @staticmethod
    def get_all_trainers(cursor) -> list[Trainer]:
        sql = "SELECT * FROM trainers"
        cursor.execute(sql)
        records = cursor.fetchall()
        trainer_list = []
        if records:
            for record in records:
                trainer_list.append(
                    Trainer(
                        id=record[0],
                        email=record[1],
                        first_name=record[2],
                        last_name=record[3],
                        admin=record[4]
                    )
                )
        if len(trainer_list) == 0:
            raise ResourceNotFound("No trainers found")
        return trainer_list

    @staticmethod
    def get_trainer_by_id(cursor, trainer_id):
        sql = "SELECT * FROM trainers WHERE id=%s"
        cursor.execute(sql, [trainer_id])
        records = cursor.fetchall()
        if records:
            record = records[0]
            return Trainer(id=record[0],
                           email=record[1],
                           first_name=record[2],
                           last_name=record[3],
                           admin=record[4])
        else:
            raise ResourceNotFound(
                "No trainer could be found with the given id")

    @staticmethod
    def get_trainers_in_batch(cursor, batch_id):
        sql = "select t.id, t.first_name, t.last_name, t.email, tb.role " \
              "from trainers as t left join trainer_batches tb " \
              "on id = trainer_id where batch_id = %s"
        cursor.execute(sql, [batch_id])
        records = cursor.fetchall()
        trainers = []
        for record in records:
            trainers.append(
                Trainer(id=record[0],
                        first_name=record[1],
                        last_name=record[2],
                        email=record[3],
                        role=record[4]))
        return trainers

    @staticmethod
    def login(cursor, email):
        sql = "SELECT * FROM trainers WHERE email=%s"
        cursor.execute(sql, [email])
        records = cursor.fetchall()
        if records:
            record = records[0]
            return Trainer(id=record[0],
                           first_name=record[2],
                           last_name=record[3],
                           email=record[1],
                           admin=record[4])
        else:
            raise ResourceNotFound("No trainer exists with those credentials")

    @staticmethod
    def get_years_for_trainer(cursor, trainer_id):
        """Takes in a year and returns all the batches currently in progress for that year"""
        sql = "SELECT b.start_date " \
              "FROM batches as b " \
              "left join trainer_batches as tb " \
              "on b.id = tb.batch_id " \
              "WHERE trainer_id = %s"
        cursor.execute(sql, [trainer_id])
        records = cursor.fetchall()
        years = set()
        for year in records:
            years.add(datetime.fromtimestamp(year[0]).year)

        return years

    @staticmethod
    def create_trainer(cursor, trainer: Trainer) -> Trainer:
        """Create a new trainer"""
        # ! For testing use only
        sql = """\
            insert into
                trainers
            values
                (default, %s, %s, %s, %s)
            returning
                id"""
        cursor.execute(sql, [
            trainer.email, trainer.first_name, trainer.last_name, trainer.admin
        ])
        trainer.id = cursor.fetchone()[0]
        return trainer

    @staticmethod
    def create_trainer_batch(cursor, trainer: Trainer, batch: Batch):
        """Create a new trainer_batch join"""
        # ! For testing use only
        sql = """\
            insert into
                trainer_batches
            values
                (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, [
            trainer.id, batch.id, batch.start_date, batch.end_date, trainer.role
        ])
        return True
