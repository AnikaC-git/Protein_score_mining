"""
Functionality to effectively interact with SQLite database where extracted data from articles will be stored into.
It contains functions to connect as well as clear the database, should it be desired to run the complete pipeline at
once, for example, for a subset of articles.
"""

import sqlite3
import sys

from sqlite3 import Error


def create_database_connection(_db_file):
    """
    Creates a connection to a database file and returns the connector. Should an error be an encountered while trying
    to connect to the database, the program is aborted.

    :param _db_file: file path to the database file that a connection should be established to
    :type: str or Path
    :return: connector to database
    :rtype: connector
    """

    try:
        conn = sqlite3.connect(_db_file)
        return conn
    except Error as e:
        print(e)
        sys.exit()
