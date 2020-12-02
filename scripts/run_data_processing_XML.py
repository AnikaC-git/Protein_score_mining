"""
Run script to trigger data processing for XML files downloaded from Pubmed. To run this script a config file is
required to specify default settings for the correct operation, mainly where to read data from and write it to. The
config file include in the data/results/example_1 folder of this project contains default settings, such as to read
from data/raw and write to data/processed. These settings can be updated according to a new structure if necessary.
"""

import sys

from data_processing.extract_publication_data import extract_publication_data_from_xml
from protein_score_utilities.convenience_functions_files import read_config
from protein_score_utilities.convenience_functions_files import read_xml_file_names
from protein_score_utilities.convenience_functions_database import create_database_connection

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No config file provided. Program will abort")
        sys.exit(1)
    elif not str(sys.argv[1]).endswith(".yml"):
        print("Config file is not in the correct format -- yaml file needed. Program will abort")
        sys.exit(1)

    config = read_config(sys.argv[1])
    fnames = read_xml_file_names(config['data_raw'])

    # todo: add handling for database reset depending on config; add message for when database is regenerated
    db_conn = create_database_connection(config['data_processed'] + config['db_file'])

    for fname in fnames:
        print(fname)
        extract_publication_data_from_xml(str(fname), db_conn)
