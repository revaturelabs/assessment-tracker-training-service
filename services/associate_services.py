from daos.daos_impl.batch_dao_impl import BatchDAOImpl
from models.associate import Associate
from daos.daos_impl.associate_dao_impl import AssociateDAOImpl
from utils.connection import Connection

conn = Connection.conn


class AssociateServices:
    associate_dao = AssociateDAOImpl()
    batch_dao = BatchDAOImpl()

    @classmethod
    def get_associated_by_id(cls, associate_id):
        with conn:
            with conn.cursor() as cursor:
                return cls.associate_dao.get_associate_by_id(
                    cursor, associate_id)

    @classmethod
    def get_associate_in_batch(cls, associate_id, batch_id):
        with conn:
            with conn.cursor() as cursor:
                return cls.associate_dao.get_associate_in_batch(
                    cursor, batch_id, associate_id)

    @classmethod
    def get_all_associates_in_batch(cls, batch_id):
        with conn:
            with conn.cursor() as cursor:
                return cls.associate_dao.get_all_associates_in_batch(
                    cursor, batch_id)

    @classmethod
    def create_associate_in_batch(cls, associate: Associate, batch_id: int):
        with conn:
            with conn.cursor() as cursor:
                associate = cls.associate_dao.create_associate(
                    cursor, associate)
                batch = cls.batch_dao.get_batch_by_id(cursor, batch_id)
                cls.associate_dao.create_associate_batch(
                    cursor, associate, batch)
                return associate
