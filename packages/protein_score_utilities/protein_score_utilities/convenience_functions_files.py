"""
Convenience functions in relation to identifying relevant files, reading config file and file handling in general.
"""


def read_config(_config: str):
    """
    Reads parameter settings required for operation from config file. Config file format is expected to be in yaml file
    format.

    :param _config: path to config file
    :return: dictionary containing parameter settings for operation
    ;rtype: dict
    """
    import yaml
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
    from pathlib import Path
    return [x for x in Path(_xml_folder).iterdir() if x.is_file() and str(x).endswith(".xml")]
