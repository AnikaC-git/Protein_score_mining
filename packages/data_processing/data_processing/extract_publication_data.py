"""
Module that provides functionality for the extraction of text passages from Pubmed XML files. These XML
files contain references for a large number of publications, where each publication may hold more or less
specifying data. As a first attempt, the data that will be extracted for each publication, if present,
are Pubmed ID, title, abstract, journal and publication year. The data will be held temporarily in
SQLite database for easier querying.

For now it is only XML files, but in the future, targeted support for PDF, docx or text files could be
added here. Though this would very likely require additional functionality to determine the structure 
of the document, e.g. through processing Core Scientific Concepts such as those described 
<a href="http://www.lrec-conf.org/proceedings/lrec2016/pdf/676_Paper.pdf">here</a>.
"""


def extract_publication_data_from_xml(file_path, database_conn):
    """
    Extracts title, abstract, journal and so on for a publication contained in the Pubmed XML file.
    Provides summary information at the end about how many publications have been identified.
    """
    # todo: the approach for identifying relevant parts of the publication is very simplistic and 
    #  not very foolproof for now and should be changed going forward
    from lxml import etree
    context = etree.iterparse(file_path, events=('end',), tag="PubmedArticle")
    elem_of_interest = {
        'PMID': 'MedlineCitation/PMID',
        'abstract': 'MedlineCitation/Article/Abstract/AbstractText',
        'title': 'MedlineCitation/Article/ArticleTitle',
        'journal': 'MedlineCitation/Article/Journal/Title',
        'pub_date_year': 'MedlineCitation/Article/Journal/JournalIssue/PubDate/Year'
    }

    counter_publications = 0
    counter_publications_incomplete = 0

    for event, elem in context:
        counter_publications += 1
        publication = {}
        for key, value in elem_of_interest.items():
            print(f"{key} {value}")
            eoi = elem.xpath(value)        
            # only take first entry found
            if len(eoi) > 0:
                publication[key] = eoi[0].text
            else:
                break
        
        if len(publication) == len(elem_of_interest):
            print(publication)
            # save_publication_to_database(publication, database_conn)
        else:
            counter_publications_incomplete += 1
        
        # deleting the element and any references to it to speed up the process of extraction
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]

    print(f"Total number of publications found: {counter_publications}")
    print(f"Total number of incomplete publications found: {counter_publications_incomplete}")
                          
                
def save_publication_to_database(data: dict, database_conn):
    """
    Save data extracted about a publication from one of the data sources to the publication database.

    :param data: publication data to be stored in database
    :type: dict
    :param database_conn: connector to database data should be stored in
    :type: conn
    :return: True if record stored successfully, otherwise False
    :rtype: bool
    """
    pass
