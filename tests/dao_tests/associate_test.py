from models.associate import Associate

from copy import copy
from daos.daos_impl.associate_dao_impl import AssociateDAOImpl
from exceptions.resource_not_found import ResourceNotFound
from utils.connection import Connection

conn = Connection.conn
associate_dao = AssociateDAOImpl()
ASSOCIATE = Associate("Testy", "McTesterson", "test@test.test", "")


def test_get_associate_by_id(self):
    with conn:
        with conn.cursor() as cursor:
            associate = copy(ASSOCIATE)
            result = associate_dao.create_associate(cursor, associate)
            retrieve = associate_dao.get_associate_by_id(cursor, result.id)
            assert result.id != retrieve.id
        conn.rollback()


# def test_get_associate_in_batch(self):
#     with conn:
#         with conn.cursor() as cursor:
#             assert associate_dao.get_associate_in_batch(cursor, 6, 4)
#         conn.rollback()

# def test_get_associate_by_id(self):
#     with conn:
#         with conn.cursor() as cursor:
#             assert associate_dao.get_associate_by_id(cursor, 5)
#         conn.rollback()

# def test_get_associate_in_batch_fail(self):
#     with conn:
#         with conn.cursor() as cursor:
#             try:
#                 associate_dao.get_associate_in_batch(cursor, 200, 200)
#                 assert False
#             except ResourceNotFound:
#                 assert True
#         conn.rollback()

# def test_get_associate_by_id_fail(self):
#     with conn:
#         with conn.cursor() as cursor:
#             try:
#                 associate_dao.get_associate_by_id(cursor, 200)
#             except ResourceNotFound:
#                 assert True
#         conn.rollback()
