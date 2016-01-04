from salttester import cmd, get_file


def run(args, logging):
    highstate_junit_file = '/tmp/highstate.xml'
    args.cmd = 'sudo salt-call state.highstate --out=junit --out-file={0}'.format(highstate_junit_file)
    args.remote_path = highstate_junit_file
    args.local_path = './highstate.xml'

    logging.info('Running highstate...')
    exit_code, stdout, stderr = cmd.run(args, logging)
    logging.info('Finished highstate...')

    logging.info('Downloading highstate results...')
    get_file.run(args, logging)
    logging.info('Finished downloading highstate results...')
    return exit_code, stdout, stderr
