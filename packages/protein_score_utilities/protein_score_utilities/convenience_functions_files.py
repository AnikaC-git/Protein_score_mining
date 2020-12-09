"""
Convenience functions in relation to identifying relevant files, reading config file and file handling in general.
"""


def read_config(config: str):
    """
    Reads parameter settings required for operation from config file. Config file format is expected to be in yaml file
    format.

    :param config: Path to config file provided as string.
    :type config: str
    :return: Dictionary containing parameter settings for operation.
    :rtype: dict
    """

    import yaml
    # todo: more elaborate error handling needed if file parser raises error
    with open(config) as file:
        # loader returns dictionary of settings specified in config file
        return yaml.load(file, Loader=yaml.FullLoader)


def read_xml_file_names(xml_folder: str):
    """
    Function to read names of XML files in specified folder. Convenience function to process multiple XML files at once.

    :param xml_folder: Folder assumed to hold XML files, with file names ending in .xml.
    :type xml_folder: str
    :return: A list of file names ending in ".xml" in the specified folder.
    :rtype: list
    """

    from pathlib import Path
    return [x for x in Path(xml_folder).iterdir() if x.is_file() and str(x).endswith(".xml")]
