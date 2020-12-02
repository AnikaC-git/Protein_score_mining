"""
Run script to trigger data processing for XML files downloaded from Pubmed. To run this script a config file is
required to specify default settings for the correct operation, mainly where to read data from and write it to. The
config file include in the data/results/example_1 folder of this project contains default settings, such as to read
from data/raw and write to data/processed. These settings can be updated according to a new structure if necessary.
"""

import sys
import yaml
from pathlib import Path

from data_processing.extract_publication_data import extract_publication_data_from_xml


def read_config(_config: str):
    """
    Reads parameter settings required for operation from config file. Config file format is expected to be in yaml file
    format.

    :param _config: path to config file
    :return: dictionary containing parameter settings for operation
    ;rtype: dict
    """
    # todo: more elaborate error handling needed if file parser raises error
    with open(_config) as file:
        # loader returns dictionary of settings specified in config file
        return yaml.load(file, Loader=yaml.FullLoader)


def read_xml_file_names(_xml_folder: str):
    """
    Function to read names of XML files in specified folder. Convenience function to process multiple XML files at once.

    :param _xml_folder: folder assumed to hold XML files with file names ending in .xml
    :type: str
    :return: a list of file names ending in ".xml" files in the specified folder
    :rtype: list
    """
    return [x for x in Path(_xml_folder).iterdir() if x.is_file() and str(x).endswith(".xml")]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No config file provided. Program will abort")
        sys.exit(1)
    elif not str(sys.argv[1]).endswith(".yml"):
        print("Config file is not in the correct format -- yaml file needed. Program will abort")
        sys.exit(1)

    config = read_config(sys.argv[1])
    fnames = read_xml_file_names(config['data_raw'])

    # todo: read from config file
    db_conn = ""

    for fname in fnames:
        print(fname)
        extract_publication_data_from_xml(str(fname), db_conn)
