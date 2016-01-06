"""
Main Module
"""
import argparse
import logging
import sys
from salttester import deploy, cmd, pytest, highstate, serverspec, terminate, userdata, get_file

ACTIONS = {'deploy': deploy,
           'cmd': cmd,
           'pytest': pytest,
           'highstate': highstate,
           'serverspec': serverspec,
           'getfile': get_file,
           'terminate': terminate}

LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}


def main():
    """
    The main executor for salttester app
    :return: An exit code
    """

    parser = create_parser()
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                        level=LEVELS[args.log_level])

    logging.debug('Inputted arguments...')
    logging.debug(args)

    # pylint: disable=W0612
    exit_code, stdout, stderr = ACTIONS[args.command].run(args, logging)
    sys.exit(exit_code)


def create_parser():
    """
    Creates the argparser object for salttester

    :return: Argparse parser object
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-b', '--build-id',
                        help='Jenkins build ID',
                        required=True)
    parser.add_argument('-o', '--os',
                        help='Choose an OS',
                        choices=[o for o in userdata.OS], required=True)
    parser.add_argument('-l', '--log-level',
                        help='Set the log level',
                        choices=[l for l in LEVELS], required=False,
                        default='info')

    subparsers = parser.add_subparsers(help='commands', dest='command')

    # Deploy Sub-parser
    deploy_parser = subparsers.add_parser('deploy',
                                          help='Deploy and build an AWS EC2 instance')
    deploy_parser.add_argument('--image-id',
                               help='AWS EC2 image ID', required=True)
    deploy_parser.add_argument('--instance-type',
                               help='AWS EC2 instance type',
                               required=True)
    deploy_parser.add_argument('--keyname',
                               help='AWS EC2 SSH key name',
                               required=True)
    deploy_parser.add_argument('--git-repo',
                               help='The url of the git repo to clone',
                               required=True)
    deploy_parser.add_argument('--git-branch',
                               help='The name of the git branch to checkout',
                               required=True)
    deploy_parser.add_argument('--subnet-id',
                               help='AWS EC2 subnet ID for regions without a default VPC',
                               required=False,
                               default=None)
    deploy_parser.add_argument('--security-group-ids',
                               help='Comma delimited list of AWS EC2 security group IDs',
                               required=False,
                               default=None)

    # Remote Sub-parser
    remote_parser = subparsers.add_parser('remote',
                                          help='Choose one of the remote actions to perform')
    remote_parser.add_argument('--username',
                               help='The ssh username',
                               required=True)
    remote_parser.add_argument('--key-filename',
                               help='The name and location of the ssh private keyfile',
                               required=True)
    remote_parser.add_argument('--port',
                               help='The ssh port',
                               required=False,
                               type=int,
                               default=22)
    remote_parser.add_argument('--timeout',
                               help='The initial ssh connection timeout in seconds',
                               required=False)

    remote_subparsers = remote_parser.add_subparsers(help='remote commands', dest='command')

    # CMD Sub-parser
    cmd_parser = remote_subparsers.add_parser('cmd',
                                              help='Execute a command on the remote instance')
    cmd_parser.add_argument('--cmd',
                            help='The command to execute on the remote instance',
                            required=True)

    # Get file Sub-parser
    getfile_parser = remote_subparsers.add_parser('getfile',
                                                  help='Gets a file from the remote instance')
    getfile_parser.add_argument('--remote-path',
                                help='The remote file to copy',
                                required=True)
    getfile_parser.add_argument('--local-path',
                                help='The destination path on the local host',
                                required=True)

    # Pytest Sub-parser
    pytest_parser = remote_subparsers.add_parser('pytest', help='Executes the py.test tests')
    pytest_parser.add_argument('--pytest-test-dir',
                               help='The directory where the py.test tests are located',
                               required=True)

    # Highstate Sub-parser
    # pylint: disable=W0612
    highstate_parser = remote_subparsers.add_parser('highstate',
                                                    help='Executes the highstate test')

    # ServerSpec Sub-parser
    serverspec_parser = remote_subparsers.add_parser('serverspec',
                                                     help='Executes the serverspec test')
    serverspec_parser.add_argument('--serverspec-test-dir',
                                   help='The directory where the serverspec tests are located',
                                   required=True)

    # Terminate Sub-parser
    # pylint: disable=W0612
    terminate_parser = subparsers.add_parser('terminate', help='Terminates the AWS EC2 instance')
    return parser

if __name__ == '__main__':
    main()
