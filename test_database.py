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
def test_database_delete_table(self,table_name, criteria):
    placeholders = [f'{column} = ?' for column in criteria.keys()]
    delete_criteria = ' AND '.join(placeholders)
    self._execute(
         f'''
         DELETE FROM {table_name}
         WHERE {delete_criteria};
         ''',
         tuple(criteria.values()), #https://www.w3schools.com/python/python_tuples.asp
     )
    assert delete_criteria == ' AND '.join(placeholders)

def test_database_select(database_manager, self, table_name, criteria=None, order_by=None):
    database_manager.select()
    criteria = criteria or {}
    
    query = f'SELECT * FROM {table_name}'
    if criteria:
        placeholders = [f'{column} = ?' for column in criteria.keys()]
        select_criteria = ' AND '.join(placeholders)
        query += f' WHERE {select_criteria}'

    if order_by:
        query += f' ORDER BY {order_by}'

    return self._execute(
        query,
        tuple(criteria.values()),
    )
    assert criteria == criteria or {}


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

def test_database_drop_table(database_manager, self, table_name):
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

    #cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='bookmarks' ''')

    cursor.execute( f''' DROP TABLE {table_name};''')

    database_manager.drop_table("bookmarks")

    assert cursor.fetchone()[0] == 1