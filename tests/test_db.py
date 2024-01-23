import pytest
import sqlite3

from db.DB import Database


def test_db_init():
    db = Database(":memory:")
    assert db.db_file == ":memory:"
    assert db.conn == None


def test_db_str():
    db = Database(":memory:")
    assert (
        str(db)
        == f"Database object for :memory:\n Connection: None\n Version: {sqlite3.version}\n"
    )


def test_db_connect():
    db = Database(":memory:")
    db.connect()
    assert db.conn != None


def test_db_close():
    db = Database(":memory:")
    db.connect()
    db.close()
    assert db.conn == None


def test_db_execute():
    db = Database(":memory:")
    db.connect()
    db.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)")
    db.execute("INSERT INTO test VALUES (1, 'test')")
    assert db.query("SELECT * FROM test") == [(1, "test")]
    db.close()


def test_db_query():
    db = Database(":memory:")
    db.connect()
    db.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)")
    db.execute("INSERT INTO test VALUES (1, 'test')")
    assert db.query("SELECT * FROM test") == [(1, "test")]
    db.close()


def test_db_create_table():
    db = Database(":memory:")
    db.connect()
    db.create_table("test", ["id INTEGER PRIMARY KEY", "name TEXT"])
    db.execute("INSERT INTO test VALUES (1, 'test')")
    assert db.query("SELECT * FROM test") == [(1, "test")]
    db.close()
