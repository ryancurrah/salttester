from paramiko import SSHClient, AutoAddPolicy
from salttester import build_data


def run(args, logging):
    hostname = build_data.read(args.build_id, 'instance', 'public_ip_address')

    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())

    logging.info('Connecting to remote host "{0}"...'.format(hostname))
    client.connect(hostname, port=args.port, username=args.username,
                   key_filename=args.key_filename, timeout=args.timeout)

    logging.info('Executing command "{0}"...'.format(args.cmd))
    stdin, stdout, stderr = client.exec_command(args.cmd)

    exit_code = stdout.channel.recv_exit_status()
    stdout = stdout.channel.makefile().read() or 'None'
    stderr = stderr.channel.makefile().read() or 'None'

    logging.info('Exit code...')
    logging.info(exit_code)
    logging.info('Standard out...')
    logging.info(stdout)
    logging.info('Standard error...')
    logging.info(stderr)
    return exit_code, stdout, stderr
