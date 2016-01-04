import ConfigParser
import os


def write(build_id, section, data):
    db_file = _db_file(build_id)
    config = ConfigParser.RawConfigParser()

    if os.path.isfile(db_file):
        config.read(db_file)

    if section not in config.sections():
        config.add_section(section)

    for key, value in data.iteritems():
        config.set(section, key, value)

    with open(db_file, 'wb') as configfile:
        config.write(configfile)


def read(build_id, section, key):
    db_file = _db_file(build_id)
    config = ConfigParser.RawConfigParser()
    config.read(db_file)
    return config.get(section, key)


def _db_file(build_id):
    db_file = '{0}.db'
    return db_file.format(build_id)
