# the database module is much more testable as its actions are largely atomic
# that said, the database module could certain be refactored to achieve decoupling
# in fact, either the implementation of the Unit of Work or just changing to sqlalchemy would be good.

import os
from datetime import datetime
import sqlite3

import pytest


from database import DatabaseManager

@pytest.fixture
def database_manager() -> DatabaseManager:
    """
    What is a fixture? https://docs.pytest.org/en/stable/fixture.html#what-fixtures-are
    """
    filename = "test_bookmarks.db"
    dbm = DatabaseManager(filename)
    # what is yield? https://www.guru99.com/python-yield-return-generator.html
    yield dbm
    dbm.__del__()           # explicitly release the database manager
    os.remove(filename)


def test_database_manager_create_table(database_manager):
    # arrange and act
    database_manager.create_table(
        "bookmarks",
        {
            "id": "integer primary key autoincrement",
            "title": "text not null",
            "url": "text not null",
            "notes": "text",
            "date_added": "text not null",
        },
    )

    #assert
    conn = database_manager.connection
    cursor = conn.cursor()

    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='bookmarks' ''')

    assert cursor.fetchone()[0] == 1

    #cleanup
    # this is probably not really needed
    database_manager.drop_table("bookmarks")


def test_database_manager_add_bookmark(database_manager):

    # arrange
    database_manager.create_table(
        "bookmarks",
        {
            "id": "integer primary key autoincrement",
            "title": "text not null",
            "url": "text not null",
            "notes": "text",
            "date_added": "text not null",
        },
    )

    data = {
        "title": "test_title",
        "url": "http://example.com",
        "notes": "test notes",
        "date_added": datetime.utcnow().isoformat()        
    }

    # act
    database_manager.add("bookmarks", data)

    # assert
    conn = database_manager.connection
    cursor = conn.cursor()
    cursor.execute(''' SELECT * FROM bookmarks WHERE title='test_title' ''')    
    assert cursor.fetchone()[0] == 1    

#Created by My
#arrange
#act
#assert
def test_database_manager_delete_bookmark(database_manager):

    # arrange
    database_manager.create_table(
        "bookmarks_delete",
        {
            "id": "integer primary key autoincrement",
            "title": "text not null",
            "url": "text not null",
            "notes": "text",
            "date_added": "text not null",
        },
    )

    data = {
        "title": "delete_title",
        "url": "http://delete.com",
        "notes": "delete notes",
        "date_added": datetime.utcnow().isoformat()        
    }

    # act
    database_manager.add("bookmarks_delete", data)

    # assert
    conn = database_manager.connection
    cursor = conn.cursor()
    cursor.execute(''' DELETE notes FROM bookmarks_delete WHERE title='delete_title' ''')    
    assert cursor.fetchone()[1] == 0 


def test_database_manager_select_table(database_manager):

    # arrange
    database_manager.create_table(
        "bookmarks_selecttable",
        {
            "id": "integer primary key autoincrement",
            "title": "text not null",
            "url": "text not null",
            "notes": "text",
            "date_added": "text not null",
        },
    )

    data = {
        "title": "selecttable_title",
        "url": "http://selecttable.com",
        "notes": "select table",
        "date_added": datetime.utcnow().isoformat()        
    }

    # act
    database_manager.add("bookmarks_selecttable", data)

    # assert
    conn = database_manager.connection
    cursor = conn.cursor()
    cursor.execute(''' SELCT * FROM bookmarks_select table WHERE title='selecttable_title' ''')    
    assert cursor.fetchone()[1] == 1


def test_database_execute(self, statement, values=None):
    with self.connection: #https://www.pythonforbeginners.com/files/with-statement-in-python
        cursor = self.connection.cursor()
        cursor.execute(statement, values or [])
        return cursor
    assert cursor == self.connection.cursor()


def test_database_add(self, table_name, data):
    placeholders = ', '.join('?' * len(data))
    column_names = ', '.join(data.keys())
    column_values = tuple(data.values())
    

    self._execute(
            f'''
            INSERT INTO {table_name}
            ({column_names})
            VALUES ({placeholders});
            ''',
            column_values,
    )

    assert column_values == tuple(data.values())

def test_database_manager_drop_table(database_manager):

    # arrange
    database_manager.create_table(
        "bookmarks_droptable",
        {
            "id": "integer primary key autoincrement",
            "title": "text not null",
            "url": "text not null",
            "notes": "text",
            "date_added": "text not null",
        },
    )

    data = {
        "title": "droptable_title",
        "url": "http://droptable.com",
        "notes": "drop table",
        "date_added": datetime.utcnow().isoformat()        
    }

    # act
    database_manager.add("bookmarks_droptable", data)

    # assert
    conn = database_manager.connection
    cursor = conn.cursor()
    cursor.execute(''' DROP TABLE FROM bookmarks_droptable WHERE title='droptable_title' ''')    
    assert cursor.fetchone()[1] == 0
