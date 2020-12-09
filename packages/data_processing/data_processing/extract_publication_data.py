"""
Module that provides functionality for the extraction of publication records. While different formats for publication
sources will be supported in the future, the only functionality available at present is for the extraction of data from
Pubmed XML files <https://pubmed.ncbi.nlm.nih.gov/help/#download-pubmed-data>`_.

These XML files contain references for a large number of publications, where each publication may hold more or less
specifying data. As a first attempt, the data that will be extracted for each publication, if present, are Pubmed ID,
title, abstract, journal and publication year. The data will be held temporarily in SQLite database for easier querying.
"""

from protein_score_utilities.convenience_functions_database import execute_insert_statement


class Publication:
    """
    Data capsule for holding data relevant to a publication.
    """

    def __init__(self, _pmid=None, _abstract_text=None, _title=None, _journal=None, _pub_year=None):
        """
        Initialising all the attributes with data provided.
        """
        self.pmid = str(_pmid) if _pmid is not None else _pmid
        self.abstract_text = str(_abstract_text) if _abstract_text is not None else _abstract_text
        self.title = str(_title) if _title is not None else _title
        self.journal = str(_journal) if _journal is not None else _journal
        self.pub_year = str(_pub_year) if _pub_year is not None else _pub_year

    def _has_all_attributes(self):
        """
        Checking whether all the required attributes for the publication have been set.

        :return: True if all the required attribures for the publication have been added, otherwise False
        :rtype: bool
        """
        return all(k is not None for k in (self.pmid, self.abstract_text, self.title, self.journal, self.pub_year))

    def save_publication_to_database(self, db_conn):
        """
        Save data extracted about a publication from one of the data sources to the publication database.

        :param data: publication data to be stored in database
        :type data: dict
        :param db_conn: connection to the database extracted publication information should be written to
        :type db_conn: :class:~`sqlite3.Connection`
        :return: True if record stored successfully, otherwise False
        :rtype: bool
        """

        stm = "INSERT INTO publications(pmid,pub_abstract,title,journal,pub_year) VALUES(?,?,?,?,?)"

        if self._has_all_attributes():
            execute_insert_statement(db_conn, stm, (self.pmid, self.abstract_text, self.title, self.journal,
                                                    self.pub_year))
            return True
        else:
            return False


def extract_publication_data_from_xml(file_path: str, db_conn):
    """
    Extracts title, abstract, journal and so on for a publication contained in the Pubmed XML file.
    Provides summary information at the end about how many publications have been identified.

    :param file_path: path to XML file from which publication data is to be extracted
    :type file_path: str
    :param db_conn: connection to the database extracted publication information should be written to
    :type db_conn: :class:~`sqlite3.Connection`
    """
    # todo: the approach for identifying relevant parts of the publication is very simplistic and 
    #  not very foolproof for now and should be changed going forward
    from lxml import etree
    try:
        context = etree.iterparse(file_path, events=('end',), tag="PubmedArticle")

        print(f"Starting data extraction for file {file_path}")

        # fields that are required for each extracted publication in order to be stored
        # key is the internal reference and value the path of the element within the XML element
        elem_of_interest = {
            'pmid': 'MedlineCitation/PMID',
            'abstract_text': 'MedlineCitation/Article/Abstract/AbstractText',
            'title': 'MedlineCitation/Article/ArticleTitle',
            'journal': 'MedlineCitation/Article/Journal/Title',
            'pub_year': 'MedlineCitation/Article/Journal/JournalIssue/PubDate/Year'
        }

        # add counters for summary stats
        counter_publications = 0
        counter_publications_incomplete = 0  # does not account for publications that might

        # go through all the publications found in the XML file
        for event, elem in context:
            counter_publications += 1
            publication = Publication()

            # attempt to extract all the relevant fields for each publication
            for key, value in elem_of_interest.items():
                eoi = elem.xpath(value)
                # only take first entry found
                # todo: this needs to be expanded, handled more carefully and details logged once logger is in place
                if len(eoi) > 0:
                    if eoi[0].text is not None:
                        publication.__setattr__(key, eoi[0].text)
                else:
                    break

            # todo: there are a number of integrity errors raised through duplicated PMIDs that would need to be
            #  further investigated
            if not publication.save_publication_to_database(db_conn):
                counter_publications_incomplete += 1

            # deleting the element and any references to it to speed up the process of extraction
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]

        # print summary statistics
        print(f"Total number of publications found: {counter_publications}")
        print(f"Total number of incomplete publications found: {counter_publications_incomplete}")
    except etree.XMLSyntaxError as e:
        print("Provided XML could not be parsed.")
