import unittest

from daos.daos_impl.batch_dao_impl import BatchDAOImpl
from exceptions.resource_not_found import ResourceNotFound
from utils.connection import Connection

conn = Connection.conn


class DAOTests(unittest.TestCase):
    def test_get_all_batches_by_year(self):
        with conn:
            with conn.cursor() as cursor:
                batches = BatchDAOImpl().get_all_batches_by_year(
                    cursor, 1, 2020)
                self.assertTrue(batches)
            conn.rollback()

    def test_get_all_batches_by_year_fail(self):
        with conn:
            with conn.cursor() as cursor:
                self.assertFalse(BatchDAOImpl().get_all_batches_by_year(
                    cursor, 1, 1))
            conn.rollback()

    def test_get_batch_by_id(self):
        with conn:
            with conn.cursor() as cursor:
                self.assertTrue(BatchDAOImpl().get_batch_by_id(cursor, 1))
            conn.rollback()

    def test_get_batch_by_id_fail(self):
        with conn:
            with conn.cursor() as cursor:
                try:
                    BatchDAOImpl().get_batch_by_id(cursor, 10000)
                    assert False
                except ResourceNotFound:
                    assert True
            conn.rollback()

    def test_search(self):
        with conn:
            with conn.cursor() as cursor:
                batches = BatchDAOImpl().search_for_batch(cursor, 1, "py")
                print(batches)
                assert batches
            conn.rollback()