"""
Functionality to effectively interact with SQLite database where extracted data from articles will be stored into.
It contains functions to connect as well as clear the database, should it be desired to run the complete pipeline at
once, for example, for a subset of articles.
"""

import sqlite3
import sys

from sqlite3 import Error
from sqlite3 import IntegrityError

def create_database_connection(db_file):
    """
    Creates a connection to a database file and returns the connector. Should an error be an encountered while trying
    to connect to the database, the program is aborted.

    :param db_file: file path to the database file that a connection should be established to
    :type db_file: str or Path
    :return: connector to database
    :rtype: connector
    """

    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        sys.exit()


def create_table(db_conn, create_table_sql: str):
    """
    Creates a connection to a database file and returns the connector. Should an error be an encountered while trying
    to connect to the database, the program is aborted.

    :param db_conn: connection to database file
    :type: connector
    :param create_table_sql: SQL statement for generating table
    :type: str
    """
    try:
        c = db_conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
        db_conn.close()
        sys.exit()


def delete_table_content(db_conn, table_name: str):
    """
    Creates a connection to a database file and returns the connector. Should an error be an encountered while trying
    to connect to the database, the program is aborted.

    :param db_conn: connection to database file
    :type: connector
    :param table_name: name of the table of which content should be deleted
    :type: str
    """

    try:
        c = db_conn.cursor()
        c.execute(f"DELETE FROM {table_name}")
    except Error as e:
        print(e)
        db_conn.close()
        sys.exit()


def execute_insert_statement(db_conn, stm: str, data: tuple):
    """
    Executes statement

    :param db_conn: connection to database file
    :type db_conn: connector
    :param stm: name of the table of which content should be deleted
    :type stm: str
    :param data: tuple containing data to be inserted into statement and consequently database
    :type data: tuple
    """

    try:
        c = db_conn.cursor()
        c.execute(stm, data)
    except IntegrityError as e:
        # errors are raised when an entry is attempted with an already existing primary key
        print(stm)
        print(data)
        pass
    except Error as e:
        print(e)
        db_conn.close()
        sys.exit()
