"""
Functionality interact with SQLite database where extracted data from articles will be stored into. For the moment,
the module contains functionality to connect to a database, create tables, delete table content and insert data into
tables.
"""

import sqlite3 as sl3
import sys


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
        conn = sl3.connect(db_file)
        return conn
    except sl3.Error as e:
        print(e)
        sys.exit()


def create_table(db_conn, create_table_sql: str):
    """
    Creates a table in the database to which a connection has been established before. Should an error be encountered
    while trying to create the table, the program is aborted.

    :param db_conn: connection to the database extracted publication information should be written to
    :type db_conn: sqlite3.Connection
    :param create_table_sql: SQL statement for generating table
    :type create_table_sql: str
    """
    try:
        c = db_conn.cursor()
        c.execute(create_table_sql)
    except sl3.Error as e:
        print(e)
        db_conn.close()
        sys.exit()


def delete_table_content(db_conn, table_name: str):
    """
    Deletes the content of a database table, e.g. when the data should be extracted afresh. Should an error be an
    encountered while trying to erase the content of the table, the program is aborted.

    :param db_conn: connection to the database extracted publication information should be written to
    :type db_conn: sqlite3.Connection
    :param table_name: name of the table of which content should be deleted
    :type table_name: str
    """

    try:
        c = db_conn.cursor()
        c.execute(f"DELETE FROM {table_name}")
    except sl3.Error as e:
        print(e)
        db_conn.close()
        sys.exit()


def execute_insert_statement(db_conn, stm: str, data: tuple):
    """
    Inserts data into a table based on the insert statement and data provided. Should an error other than
    IntegrityErrors (e.g. through duplicated primary keys be encountered), the program will be aborted.

    :param db_conn: connection to database file
    :type db_conn: sqlite3.Connection
    :param stm: name of the table of which content should be deleted
    :type stm: str
    :param data: tuple containing data to be inserted into statement and consequently database
    :type data: tuple
    """

    try:
        c = db_conn.cursor()
        c.execute(stm, data)
    except sl3.IntegrityError as e:
        # errors are raised when an entry is attempted with an already existing primary key
        # todo: this is at the moment to support import to continue with existing data issues; going forward better
        #  handling of the data issues should be decided after investigation
        print(stm)
        print(data)
        pass
    except sl3.Error as e:
        print(e)
        db_conn.close()
        sys.exit()
