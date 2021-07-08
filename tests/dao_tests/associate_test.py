import unittest

from daos.daos_impl.associate_dao_impl import AssociateDAOImpl
from exceptions.resource_not_found import ResourceNotFound
from utils.connection import Connection

conn = Connection.conn
associate_dao = AssociateDAOImpl()


class AssociateTest(unittest.TestCase):
    def test_get_associate_in_batch(self):
        with conn:
            with conn.cursor() as cursor:
                assert associate_dao.get_associate_in_batch(cursor, 6, 4)
            conn.rollback()

    def test_get_associate_by_id(self):
        with conn:
            with conn.cursor() as cursor:
                assert associate_dao.get_associate_by_id(cursor, 5)
            conn.rollback()

    def test_get_associate_in_batch_fail(self):
        with conn:
            with conn.cursor() as cursor:
                try:
                    associate_dao.get_associate_in_batch(cursor, 200, 200)
                    assert False
                except ResourceNotFound:
                    assert True
            conn.rollback()

    def test_get_associate_by_id_fail(self):
        with conn:
            with conn.cursor() as cursor:
                try:
                    associate_dao.get_associate_by_id(cursor, 200)
                except ResourceNotFound:
                    assert True
            conn.rollback()