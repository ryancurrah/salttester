"""
Pytest Test Runner
"""
from salttester import cmd, get_file


def run(args, logging):
    """
    Runs the pytest test runner and downloads the test result

    :param args: A NameSpace object with the arguments required
    :param logging: A python logging object
    :return: An exit code
    """
    pytest_junit_file = '/tmp/pytest.xml'
    args.cmd = 'sudo py.test {0} -v --junit-xml={1}'.format(args.pytest_test_dir, pytest_junit_file)
    args.remote_path = pytest_junit_file
    args.local_path = './pytest.xml'

    logging.info('Running py.test...')
    exit_code, stdout, stderr = cmd.run(args, logging)
    logging.info('Finished py.test...')

    logging.info('Downloading py.test results...')
    get_file.run(args, logging)
    logging.info('Finished downloading py.test results...')
    return exit_code, stdout, stderr
