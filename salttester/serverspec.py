"""
ServerSpec Test Runner
"""


def run(args, logging):
    """
    Runs the serverspec test runner and downloads the test result

    :param args: A NameSpace object with the arguments required
    :param logging: A python logging object
    :return: An exit code
    """
    args.cmd = 'run some serverspec tests'
    logging.info('Running serverpec test')

