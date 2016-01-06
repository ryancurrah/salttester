"""
Build Data File Generator and Reader
"""
import ConfigParser
import os


def write(build_id, section, data):
    """
    Writes key value data to an ini type file

    :param build_id: The ID of the build which will be used as part of the filename
    :param section: The name of the ini file section to place the data in
    :param data: A dictionary of the key value data to store
    :return: The db file name
    """
    db_file = db_file_name(build_id)
    config = ConfigParser.RawConfigParser()

    if os.path.isfile(db_file):
        config.read(db_file)

    if section not in config.sections():
        config.add_section(section)

    for key, value in data.iteritems():
        config.set(section, key, value)

    with open(db_file, 'wb') as config_file:
        config.write(config_file)
    return db_file


def read(build_id, section, key):
    """
    Gets a key's value from a ini type file

    :param build_id: The ID of the build which will be used as part of the filename
    :param section: The name of the ini file section to place the data in
    :param key: The name of the key to retrieve
    :return: The key value or None
    """
    db_file = db_file_name(build_id)
    config = ConfigParser.RawConfigParser()
    config.read(db_file)
    return config.get(section, key)


def db_file_name(build_id):
    """
    Generates a file name for the build data file using the build_id

    :param build_id: The ID of the build which will be used as part of the filename
    :return: Build file name
    """
    db_file = '{0}.db'
    return db_file.format(build_id)
