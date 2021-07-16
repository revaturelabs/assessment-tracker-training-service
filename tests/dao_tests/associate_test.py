from copy import copy
from daos.daos_impl.associate_dao_impl import AssociateDAOImpl as a
from daos.daos_impl.batch_dao_impl import BatchDAOImpl as b
from exceptions.resource_not_found import ResourceNotFound
from models.associate import Associate
from models.batch import Batch
from pytest import raises
from utils.connection import Connection

conn = Connection().conn
ASSOCIATE = Associate("Testy", "McTesterson", "test@test.test", "")
BATCH = Batch("Batchy", "Snek", 1625788800, 1631145600)


def test_get_associate_by_id():
    with conn:
        with conn.cursor() as cursor:
            associate = copy(ASSOCIATE)
            result = a.create_associate(cursor, associate)
            retrieve = a.get_associate_by_id(cursor, result.id)
            assert result.first_name == retrieve.first_name
        conn.rollback()


def test_get_all_associates():
    with conn:
        with conn.cursor() as cursor:
            associate = copy(ASSOCIATE)
            a.create_associate(cursor, associate)
            results = a.get_all_associates(cursor)
            assert len(results) >= 1
        conn.rollback()


def test_get_associate_by_id_fail():
    with conn:
        with conn.cursor() as cursor:
            associate = copy(ASSOCIATE)
            a.create_associate(cursor, associate)

            # with pytest.raises() ensures a specific exception occurs,
            # and will raise an exception if it does not occur.
            with raises(ResourceNotFound):
                a.get_associate_by_id(cursor, 0)
        conn.rollback()


def test_get_associate_in_batch():
    with conn:
        with conn.cursor() as cursor:
            associate = copy(ASSOCIATE)
            batch = copy(BATCH)
            associate.id = a.create_associate(cursor, associate).id
            batch.id = b.create_batch(cursor, batch).id
            a.create_associate_batch(cursor, associate, batch)
            result = a.get_associate_in_batch(cursor, associate.id, batch.id)
            assert associate.first_name == result.first_name
        conn.rollback()


def test_get_associate_in_batch_fail():
    with conn:
        with conn.cursor() as cursor:
            associate = copy(ASSOCIATE)
            batch = copy(BATCH)
            associate.id = a.create_associate(cursor, associate).id
            batch.id = b.create_batch(cursor, batch).id
            a.create_associate_batch(cursor, associate, batch)
            with raises(ResourceNotFound):
                a.get_associate_in_batch(cursor, 0, 0)
        conn.rollback()


def test_batch_create_associate_batch():
    with conn:
        with conn.cursor() as cursor:
            associates = [copy(ASSOCIATE) for _ in range(5)]
            batch = copy(BATCH)
            batch.id = b.create_batch(cursor, batch).id
            for associate in associates:
                associate.id = a.create_associate(cursor, associate).id
            a.batch_create_associate_batch(
                cursor, [associate.id for associate in associates], batch,
                "In Progress")
            associate_count = 0
            for associate in associates:
                if a.get_associate_by_id(cursor, associate.id).id > 0:
                    associate_count += 1
            assert associate_count == 5
        conn.rollback()
