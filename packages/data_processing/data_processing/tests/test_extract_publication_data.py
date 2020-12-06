import sqlite3

from io import StringIO
from unittest import TestCase
from pathlib import Path

from data_processing.extract_publication_data import extract_publication_data_from_xml
from data_processing.extract_publication_data import save_publication_to_database


class TestExtractPublicationDataFromXML(TestCase):
    """
    All tests relating to :func:~`data_processing.extract_publication_data.extract_publication_data_from_xml` in the
    data_processing package.
    """
    def setUp(self) -> None:
        """
        Creating database setup (ie. connection to database and table "publications" existing for function to write to.
        """
        self.db_file = Path.joinpath(Path(__file__).parent, "test_extract_publication_data_from_xml.db")
        self.db_conn = sqlite3.connect(self.db_file)
        cur = self.db_conn.cursor()
        # create table if needed
        cur.execute(
            "CREATE TABLE IF NOT EXISTS publications (pmid integer PRIMARY KEY, " \
            "pub_abstract text NOT NULL, journal text NOT NULL, title text NOT NULL, " \
            "pub_year text NOT NULL);"
        )
        # delete table content just in case ...
        cur.execute("DELETE FROM publications;")

    def test_extract_publication_data_from_empty_xml(self):
        """
        Pass empty string as XML.
        :return:
        """
        pass

    def test_extract_publication_data_from_xml_valid_xml(self):
        """
        Pass correct and complete XML.
        :return:
        """
        xml = ""
        # extract_publication_data_from_xml(StringIO(xml), self.db_conn)
        pass

    def text_extract_publication_data_from_xml_incomplete_record(self):
        """
        Pass XML without one of the required attributes missing.
        :return:
        """
        pass

    def tearDown(self) -> None:
        """
        Close database connection and clear all content.
        :return:
        """
        cur = self.db_conn.cursor()
        # delete table content just in case ...
        cur.execute("DELETE FROM publications;")
        self.db_conn.close()



class TestSavePublicationToDatabase(TestCase):
    """
    All tests relating to :func:~`data_processing.extract_publication_data.save_publication_to_database` in the
    data_processing package.
    """
    def setUp(self) -> None:
        pass

    def test_save_publication_to_database_correct(self):
        pass

    def test_save_publication_to_database_incomplete_record(self):
        pass

    def test_save_publication_to_database_type_error(self):
        pass

    def test_save_publication_to_database_double(self):
        pass


if __name__ == "__main__":
    TestExtractPublicationDataFromXML.main()
    TestSavePublicationToDatabase.main()