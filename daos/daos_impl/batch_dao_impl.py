from daos.batch_dao import BatchDAO
from exceptions.resource_not_found import ResourceNotFound
from models.batch import Batch
from utils.connection import Connection

conn = Connection.conn


class BatchDAOImpl(BatchDAO):
    @staticmethod
    def get_batch_by_id(cursor, batch_id):
        """Takes in an id for a batch record and returns a Batch object"""
        sql = "SELECT * FROM batches where id=%s"
        cursor.execute(sql, [batch_id])
        records = cursor.fetchall()
        if records:
            record = records[0]
            return Batch(id=record[0],
                         start_date=record[1],
                         end_date=record[2],
                         name=record[3],
                         training_track=record[4])
        else:
            raise ResourceNotFound("No batch could be found with the given id")

    @staticmethod
    def get_all_batches_by_year(cursor, trainer_id, year):
        """Takes in a year and returns all the batches currently in progress for that year"""
        sql = "SELECT b.id, b.start_date, b.end_date, b.name, b.training_track " \
              "FROM batches as b " \
              "left join trainer_batches as tb " \
              "on b.id = tb.batch_id " \
              "WHERE trainer_id = %s and date_part('year', b.start_date) = %s"
        cursor.execute(sql, [trainer_id, year])
        records = cursor.fetchall()
        batches = []
        for batch in records:
            batches.append(
                Batch(id=batch[0],
                      start_date=batch[1],
                      end_date=batch[2],
                      name=batch[3],
                      training_track=batch[4]))
        return batches

    @staticmethod
    def search_for_batch(cursor, trainer_id, track):
        """Searches for batch by trainer and track"""
        sql = "SELECT b.id, b.start_date, b.end_date, b.name, b.training_track " \
              "FROM batches as b " \
              "left join trainer_batches as tb " \
              "on b.id = tb.batch_id " \
              "WHERE trainer_id = %s and LOWER(training_track) like LOWER(%s)"
        cursor.execute(sql, [trainer_id, track + "%"])
        records = cursor.fetchall()
        batches = []
        for batch in records:
            batches.append(
                Batch(id=batch[0],
                      start_date=batch[1],
                      end_date=batch[2],
                      name=batch[3],
                      training_track=batch[4]))
        return batches
