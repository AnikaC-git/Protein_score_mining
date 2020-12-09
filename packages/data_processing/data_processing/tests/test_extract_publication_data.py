import sqlite3

from io import BytesIO
from unittest import TestCase
from pathlib import Path

from data_processing.extract_publication_data import extract_publication_data_from_xml
from data_processing.extract_publication_data import Publication


def setup_db_conn():
    """
    Sets up connection to test database and adds publication table if needed.
    :return: connection to test database
    :rtype: sqlite3.Connection
    """
    test_db_file = Path.joinpath(Path(__file__).parent, "test_extract_publication_data_from_xml.db")
    test_db_conn = sqlite3.connect(test_db_file)
    cur = test_db_conn.cursor()
    # create table if needed
    cur.execute(
        "CREATE TABLE IF NOT EXISTS publications (pmid integer PRIMARY KEY, " \
        "pub_abstract text NOT NULL, journal text NOT NULL, title text NOT NULL, " \
        "pub_year text NOT NULL);"
    )
    # delete table content just in case ...
    cur.execute("DELETE FROM publications;")
    return test_db_conn


def shutdown_db_conn(test_db_conn):
    """
    Cleans all records that may have been added to the publication table and disconnects from the database.
    :param test_db_conn: connection to database
    :type test_db_conn: sqlite3.Connection
    """
    cur = test_db_conn.cursor()
    # delete table content just in case ...
    cur.execute("DELETE FROM publications;")
    test_db_conn.close()


class TestExtractPublicationDataFromXML(TestCase):
    """
    All tests relating to :func:~`data_processing.extract_publication_data.extract_publication_data_from_xml` in the
    data_processing package.
    """
    def setUp(self) -> None:
        """
        Creating database setup (ie. connection to database and table "publications" existing) for test function
        to write to.
        """
        self.test_db_conn = setup_db_conn()

    def test_extract_publication_data_from_empty_xml(self):
        """
        Checks whether an empty file can be passed safely to the data extraction function.
        """
        xml = ("").encode(encoding="UTF-8")
        extract_publication_data_from_xml(BytesIO(xml), self.test_db_conn)

    def test_extract_publication_data_from_xml_valid_xml(self):
        """
        Tests whether correct XML string is processed without error and written to database.
        """
        xml = ("<PubmedArticle><MedlineCitation>"
               "<PMID>4325</PMID>"
               "<Article>"
               "<ArticleTitle>article title</ArticleTitle>"
               "<Abstract><AbstractText>abstract text</AbstractText></Abstract>"
               "<Journal>"
               "<Title>journal name</Title>"
               "<JournalIssue><PubDate><Year>2020</Year></PubDate></JournalIssue>"
               "</Journal>"
               "</Article>"
               "</MedlineCitation></PubmedArticle>").encode(encoding="UTF-8")
        extract_publication_data_from_xml(BytesIO(xml), self.test_db_conn)

    def test_extract_publication_data_from_xml_incomplete_record(self):
        """
        Pass XML without one of the required attributes missing.
        """
        xml = ("<PubmedArticle><MedlineCitation>"
               "<PMID>4325</PMID>"
               "<Article>"
               "<ArticleTitle>article title</ArticleTitle>"
               "<Journal>"
               "<Title>journal name</Title>"
               "<JournalIssue><PubDate><Year>2020</Year></PubDate></JournalIssue>"
               "</Journal>"
               "</Article>"
               "</MedlineCitation></PubmedArticle>").encode(encoding="UTF-8")
        extract_publication_data_from_xml(BytesIO(xml), self.test_db_conn)

    def tearDown(self) -> None:
        """
        Disconnecting from database after test finished.
        """
        if self.test_db_conn:
            shutdown_db_conn(self.test_db_conn)


class TestPublication(TestCase):
    """
    All tests relating to class :class:~`data_processing.extract_publication_data.Publication` in the
    data_processing package.
    """
    def setUp(self) -> None:
        pass

    def test_has_all_attributes_empty_record(self):
        """
        Checks whether :func:~`data_processing.extract_publication_data.Publication.has_all_attributes` returns False
        for an empty publication record.
        """
        test_pub = Publication()
        self.assertEqual(False, test_pub._has_all_attributes())

    def test_has_all_attributes_partial_record(self):
        """
        Checks whether :func:~`data_processing.extract_publication_data.Publication.has_all_attributes` returns False
        for a partially completed publication record.
        """
        test_pub = Publication(_pmid="12345", _title="a title", _abstract_text="an abstract")
        self.assertEqual(False, test_pub._has_all_attributes())

    def test_has_all_attributes_full_record(self):
        """
        Checks whether :func:~`data_processing.extract_publication_data.Publication.has_all_attributes` returns True
        for a completed publication record.
        """
        test_pub = Publication(_pmid="12345", _title="a title", _abstract_text="an abstract", _journal="A journal",
                               _pub_year=2017)
        self.assertEqual(True, test_pub._has_all_attributes())

    def test_save_publication_to_database_correct(self):
        """
        Checks whether complete record is successfully written to database.
        """
        test_db_conn = setup_db_conn()
        test_pub = Publication(_pmid="12345", _title="a title", _abstract_text="an abstract", _journal="A journal",
                               _pub_year=2017)
        self.assertEqual(True, test_pub.save_publication_to_database(test_db_conn))
        shutdown_db_conn(test_db_conn)

    def test_save_publication_to_database_incomplete_record(self):
        """
        Checks whether complete record is successfully written to database.
        """
        test_db_conn = setup_db_conn()
        test_pub = Publication(_pmid="12345", _title="a title", _abstract_text="an abstract")
        self.assertEqual(False, test_pub.save_publication_to_database(test_db_conn))
        shutdown_db_conn(test_db_conn)


if __name__ == "__main__":
    TestExtractPublicationDataFromXML.main()
    TestPublication.main()
