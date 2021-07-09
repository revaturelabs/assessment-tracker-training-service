from models.batch import Batch
from daos.associate_dao import AssociateDAO
from exceptions.resource_not_found import ResourceNotFound
from models.associate import Associate


class AssociateDAOImpl(AssociateDAO):

    @staticmethod
    def get_associate_by_id(cursor, associate_id):
        """Get a specific Associate by their ID"""
        sql = "SELECT * FROM associates where id=%s"
        cursor.execute(sql, [associate_id])
        records = cursor.fetchall()
        if records:
            # only get the first record returned
            record = records[0]
            return Associate(id=record[0],
                             email=record[1],
                             first_name=record[2],
                             last_name=record[3],
                             training_status="")
        else:
            raise ResourceNotFound("No associate found with that id")

    @staticmethod
    def get_associate_in_batch(cursor, associate_id, batch_id):
        """Get an  Associate in a batch by  their ID and a batch ID"""
        sql = "select a.id, a.first_name, a.last_name, a.email, ab.training_status " \
              "from associates as a left join associate_batches ab " \
              "on id = associate_id where associate_id = %s and batch_id = %s"
        cursor.execute(sql, [associate_id, batch_id])
        records = cursor.fetchall()
        if records:
            record = records[0]
            return Associate(id=record[0],
                             first_name=record[1],
                             last_name=record[2],
                             email=record[3],
                             training_status=record[4])
        else:
            raise ResourceNotFound(
                "No associate could be found with that id and/or batch")

    @staticmethod
    def get_all_associates_in_batch(cursor, batch_id):
        """Get an all Associates in a batch by a batch ID"""
        sql = "select a.id, a.first_name, a.last_name, a.email, ab.training_status " \
              "from associates as a left join associate_batches ab " \
              "on id = associate_id where batch_id = %s"
        cursor.execute(sql, [batch_id])
        records = cursor.fetchall()
        associates = []
        if records:
            for associate in records:
                associates.append(
                    Associate(id=associate[0],
                              first_name=associate[1],
                              last_name=associate[2],
                              email=associate[3],
                              training_status=associate[4]))
            return associates
        else:
            raise ResourceNotFound("No batch could be found with that id")

    @staticmethod
    def create_associate(cursor, associate: Associate) -> Associate:
        """Create a new associate"""
        sql = """\
            insert into
                associates
            values
                (default, %s, %s, %s)
            returning
                id"""
        cursor.execute(
            sql, [associate.email, associate.first_name, associate.last_name])
        associate.id = cursor.fetchone()[0]
        return associate

    @staticmethod
    def create_associate_batch(cursor, associate: Associate, batch: Batch):
        """Create a new associate_batch join"""
        sql = """\
            insert into
                associate_batches
            values
                (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, [
            associate.id, batch.id, batch.start_date, batch.end_date,
            associate.training_status
        ])
        return True
