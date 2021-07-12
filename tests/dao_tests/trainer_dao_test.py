from copy import copy
from models.batch import Batch
from models.trainer import Trainer
from pytest import raises
from daos.daos_impl.trainer_dao_impl import TrainerDAOImpl as t
from daos.daos_impl.batch_dao_impl import BatchDAOImpl as b
from exceptions.resource_not_found import ResourceNotFound
from utils.connection import Connection

conn = Connection().conn

BATCH = Batch("TestBatch", "Python Automation", 1625788800, 1631145600)
TRAINER = Trainer("Trainer", "McTrainerFace", "i@like.trains")


def test_get_trainer_by_id():
    with conn:
        with conn.cursor() as cursor:
            trainer = copy(TRAINER)
            result = t.create_trainer(cursor, trainer)
            retrieve = t.get_trainer_by_id(cursor, result.id)
            assert result.first_name == retrieve.first_name
        conn.rollback()


def test_get_trainers_in_batch():
    with conn:
        with conn.cursor() as cursor:
            trainer = copy(TRAINER)
            batch = copy(BATCH)
            trainer.id = t.create_trainer(cursor, trainer).id
            batch.id = b.create_batch(cursor, batch).id
            t.create_trainer_batch(cursor, trainer, batch, "Yes")
            trainers = t.get_trainers_in_batch(cursor, batch.id)
            assert len(trainers) != 0
        conn.rollback()


def test_login():
    with conn:
        with conn.cursor() as cursor:
            trainer = copy(TRAINER)
            trainer.id = t.create_trainer(cursor, trainer).id
            result = t.login(cursor, "i@like.trains")
            assert result.id == trainer.id
        conn.rollback()


def test_get_trainer_by_id_fail():
    with conn:
        with conn.cursor() as cursor:
            trainer = copy(TRAINER)
            t.create_trainer(cursor, trainer)
            with raises(ResourceNotFound):
                t.get_trainer_by_id(cursor, 0)
        conn.rollback()


def test_get_trainers_in_batch_fail():
    with conn:
        with conn.cursor() as cursor:
            trainer = copy(TRAINER)
            batch = copy(BATCH)
            trainer.id = t.create_trainer(cursor, trainer).id
            batch.id = b.create_batch(cursor, batch).id
            t.create_trainer_batch(cursor, trainer, batch, "Yes")
            trainers = t.get_trainers_in_batch(cursor, 0)
            assert len(trainers) == 0
        conn.rollback()


def test_login_fail():
    with conn:
        with conn.cursor() as cursor:
            trainer = copy(TRAINER)
            trainer.id = t.create_trainer(cursor, trainer).id
            with raises(ResourceNotFound):
                t.login(cursor, "im@a.potato")
        conn.rollback()


def test_get_years_for_trainer():
    with conn:
        with conn.cursor() as cursor:
            trainer = copy(TRAINER)
            batch = copy(BATCH)
            trainer.id = t.create_trainer(cursor, trainer).id
            batch.id = b.create_batch(cursor, batch).id
            t.create_trainer_batch(cursor, trainer, batch, "Yes")
            results = t.get_years_for_trainer(cursor, trainer.id)
            assert len(results) != 0
        conn.rollback()
