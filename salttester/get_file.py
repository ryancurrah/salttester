from paramiko import SSHClient, AutoAddPolicy
from salttester import build_data


def run(args, logging):
    hostname = build_data.read(args.build_id, 'instance', 'public_ip_address')

    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())

    logging.info('Connecting to remote host "{0}"...'.format(hostname))
    client.connect(hostname, port=args.port, username=args.username,
                   key_filename=args.key_filename, timeout=args.timeout)

    logging.info('Getting file "{0}"...'.format(args.remote_path))
    sftp_client = client.open_sftp()
    sftp_client.get(args.remote_path, args.local_path)
