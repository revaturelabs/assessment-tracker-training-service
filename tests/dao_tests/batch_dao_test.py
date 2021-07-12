from copy import copy
from models.trainer import Trainer
from daos.daos_impl.batch_dao_impl import BatchDAOImpl as b
from daos.daos_impl.trainer_dao_impl import TrainerDAOImpl as t
from exceptions.resource_not_found import ResourceNotFound
from models.batch import Batch
from utils.connection import Connection
import psycopg2
import pytest

conn = Connection().conn
TEST_BATCH = Batch("TestBatch", "Python Automation", 1625788800, 1631145600)
TRAINER = Trainer("Trainer", "McTrainerFace", "i@like.trains")


def test_create_batch():
    test_batch: Batch = copy(TEST_BATCH)
    with conn:
        with conn.cursor() as cursor:
            test_batch = b.create_batch(cursor, test_batch)
            assert test_batch.id != -1
        conn.rollback()


def test_invalid_date_format_create_batch():
    with pytest.raises(psycopg2.errors.InvalidDatetimeFormat):
        test_batch: Batch = Batch("TestBatch2", "Baking", "start_date",
                                  "end_date")
        with conn:
            with conn.cursor() as cursor:
                test_batch = b.create_batch(cursor, test_batch)


def test_invalid_date_value_create_batch():
    with pytest.raises(ValueError):
        test_batch: Batch = Batch("TestBatch2", "Baking", 1639008000,
                                  1625843430)
        with conn:
            with conn.cursor() as cursor:
                test_batch = b.create_batch(cursor, test_batch)


def test_get_all_batches_by_year():
    with conn:
        with conn.cursor() as cursor:
            trainer = copy(TRAINER)
            trainer.id = t.create_trainer(cursor, trainer).id
            batch = copy(TEST_BATCH)
            batch.id = b.create_batch(cursor, batch).id
            t.create_trainer_batch(cursor, trainer, batch, "Yes")
            batches = b.get_all_batches_by_year(cursor, trainer.id, 2021)
            assert len(batches) != 0
        conn.rollback()


def test_get_all_batches_by_year_fail():
    with conn:
        with conn.cursor() as cursor:
            trainer = copy(TRAINER)
            trainer.id = t.create_trainer(cursor, trainer).id
            batch = copy(TEST_BATCH)
            batch.id = b.create_batch(cursor, batch).id
            t.create_trainer_batch(cursor, trainer, batch, "Yes")
            batches = b.get_all_batches_by_year(cursor, trainer.id, 0)
            assert len(batches) == 0
        conn.rollback()


def test_get_batch_by_id():
    with conn:
        with conn.cursor() as cursor:
            batch = copy(TEST_BATCH)
            batch.id = b.create_batch(cursor, batch).id
            result = b.get_batch_by_id(cursor, batch.id)
            assert result.name == batch.name
        conn.rollback()


def test_get_batch_by_id_fail():
    with conn:
        with conn.cursor() as cursor:
            batch = copy(TEST_BATCH)
            b.create_batch(cursor, batch).id
            with pytest.raises(ResourceNotFound):
                b.get_batch_by_id(cursor, 0)
        conn.rollback()


def test_search():
    with conn:
        with conn.cursor() as cursor:
            trainer = copy(TRAINER)
            trainer.id = t.create_trainer(cursor, trainer).id
            batch = copy(TEST_BATCH)
            batch.id = b.create_batch(cursor, batch).id
            t.create_trainer_batch(cursor, trainer, batch, "Yes")
            result = b.search_for_batch(cursor, trainer.id, "Python")
            assert len(result) != 0
        conn.rollback()
