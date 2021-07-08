from daos.daos_impl.associate_dao_impl import AssociateDAOImpl
from utils.connection import Connection

conn = Connection.conn


class AssociateServices:
    associate_dao = AssociateDAOImpl()

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
