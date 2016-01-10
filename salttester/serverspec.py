"""
ServerSpec Test Runner
"""
from salttester import cmd, get_file


def run(args, logging):
    """
    Runs the serverspec test runner and downloads the test result

    WARNING: Requires the ruby gem yarjuf and requires modification to
    your .rspec and spec_helper files to export results as junit see
    https://github.com/natritmeyer/yarjuf#modifying-the-rspec-file and
    https://github.com/natritmeyer/yarjuf#modifying-the-specspec_helperrb-file

    :param args: A NameSpace object with the arguments required
    :param logging: A python logging object
    :return: An exit code
    """
    serverspec_junit_file = '/tmp/serverspec.xml'
    args.cmd = 'cd {0}; sudo rspec -f JUnit -o {1}'.format(args.serverspec_test_dir,
                                                           serverspec_junit_file)
    args.remote_path = serverspec_junit_file
    args.local_path = './serverspec.xml'

    logging.info('Running serverspec...')
    exit_code, stdout, stderr = cmd.run(args, logging)
    logging.info('Finished serverspec...')

    logging.info('Downloading serverspec results...')
    get_file.run(args, logging)
    logging.info('Finished downloading serverspec results...')
    return exit_code, stdout, stderr
