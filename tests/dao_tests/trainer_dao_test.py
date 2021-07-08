import unittest

from daos.daos_impl.trainer_dao_impl import TrainerDAOImpl
from exceptions.resource_not_found import ResourceNotFound
from utils.connection import Connection

conn = Connection.conn


class DAOTests(unittest.TestCase):
    def test_get_trainer_by_id(self):
        with conn:
            with conn.cursor() as cursor:
                trainers = TrainerDAOImpl().get_trainer_by_id(cursor, 1)
                self.assertTrue(trainers)
            conn.rollback()

    def test_get_trainers_in_batch(self):
        with conn:
            with conn.cursor() as cursor:
                trainers = TrainerDAOImpl().get_trainers_in_batch(cursor, 1)
                self.assertTrue(trainers)
            conn.rollback()

    def test_login(self):
        with conn:
            with conn.cursor() as cursor:
                self.assertTrue(TrainerDAOImpl().login(cursor,
                                                       "rs@revature.com"))
            conn.rollback()

    def test_get_trainer_by_id_fail(self):
        with conn:
            with conn.cursor() as cursor:
                try:
                    TrainerDAOImpl().get_trainer_by_id(cursor, 20000)
                    assert False
                except ResourceNotFound:
                    assert True
            conn.rollback()

    def test_get_trainers_in_batch_fail(self):
        with conn:
            with conn.cursor() as cursor:
                trainers = TrainerDAOImpl().get_trainers_in_batch(cursor, 100)
                self.assertFalse(trainers)
            conn.rollback()

    def test_login_fail(self):
        with conn:
            with conn.cursor() as cursor:
                try:
                    TrainerDAOImpl().login(cursor, "loremipsum")
                    assert False
                except ResourceNotFound:
                    assert True
            conn.rollback()

    def test_get_years_for_trainer(self):
        with conn:
            with conn.cursor() as cursor:
                assert TrainerDAOImpl().get_years_for_trainer(cursor, 1)
            conn.rollback()