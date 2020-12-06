from unittest import TestCase

from data_processing.extract_publication_data import extract_publication_data_from_xml
from data_processing.extract_publication_data import save_publication_to_database


class TestExtractPublicationDataFromXML(TestCase):
    """
    All tests relating to :func:~`data_processing.extract_publication_data.extract_publication_data_from_xml` in the
    data_processing package.
    """

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
        pass

    def text_extract_publication_data_from_xml_incomplete_record(self):
        """
        Pass XML without one of the required attributes missing.
        :return:
        """
        pass


class TestSavePublicationToDatabase(TestCase):
    """
    All tests relating to :func:~`data_processing.extract_publication_data.save_publication_to_database` in the
    data_processing package.
    """
    def test_save_publication_to_database_correct(self):
        pass

    def test_save_publication_to_database_incomplete_record(self):
        pass

    def test_save_publication_to_database_type_error(self):
        pass

    def test_save_publication_to_database_double(self):
        pass
