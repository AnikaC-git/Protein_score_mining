"""
Module that provides functionality for the extraction of publication records. While different formats for publication
sources will be supported in the future, the only functionality available at present is for the extraction of data from
<a href="https://pubmed.ncbi.nlm.nih.gov/help/#download-pubmed-data">Pubmed XML files</a>.

These XML files contain references for a large number of publications, where each publication may hold more or less
specifying data. As a first attempt, the data that will be extracted for each publication, if present, are Pubmed ID,
title, abstract, journal and publication year. The data will be held temporarily in SQLite database for easier querying.
"""


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
    context = etree.iterparse(file_path, events=('end',), tag="PubmedArticle")

    # fields that are required for each extracted publication in order to be stored
    # key is the internal reference and value the path of the element within the XML element
    elem_of_interest = {
        'PMID': 'MedlineCitation/PMID',
        'abstract': 'MedlineCitation/Article/Abstract/AbstractText',
        'title': 'MedlineCitation/Article/ArticleTitle',
        'journal': 'MedlineCitation/Article/Journal/Title',
        'pub_date_year': 'MedlineCitation/Article/Journal/JournalIssue/PubDate/Year'
    }

    # add counters for summary stats
    counter_publications = 0
    counter_publications_incomplete = 0

    # go through all the publications found in the XML file
    for event, elem in context:
        counter_publications += 1
        publication = {}

        # attempt to extract all the relevant fields for each publication
        for key, value in elem_of_interest.items():
            eoi = elem.xpath(value)        
            # only take first entry found
            # todo: this needs to be expanded, handled more carefully and details logged once logger is in place
            if len(eoi) > 0:
                if eoi[0].text is not None:
                    publication[key] = eoi[0].text
            else:
                break

        # only store publication in database if all the relevant data fields have been extracted
        if len(publication) == len(elem_of_interest):
            save_publication_to_database(publication, db_conn)
        else:
            counter_publications_incomplete += 1
        
        # deleting the element and any references to it to speed up the process of extraction
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]

    # print summary statistics
    print(f"Total number of publications found: {counter_publications}")
    print(f"Total number of incomplete publications found: {counter_publications_incomplete}")
                          
                
def save_publication_to_database(data: dict, db_conn):
    """
    Save data extracted about a publication from one of the data sources to the publication database.

    :param data: publication data to be stored in database
    :type data: dict
    :param db_conn: connection to the database extracted publication information should be written to
    :type db_conn: :class:~`sqlite3.Connection`
    :return: True if record stored successfully, otherwise False
    :rtype: bool
    """
    c = db_conn.cursor()
    stm = f"INSERT INTO publications(pmid,pub_abstract,title,journal,pub_year) " \
          f"VALUES(?,?,?,?,?)"

    try:
        c.execute(stm, (data['PMID'], data['abstract'], data['title'], data['journal'], data['pub_date_year']))
    except Exception as e:
        pass
