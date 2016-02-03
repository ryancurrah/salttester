"""
Instance Deployment Creator
"""
import time
import boto3
from salttester import build_data, userdata


def run(args, logging):
    """
    Starts an AWS EC2 Instance using the boto3 api and passes userdata that will...

    1. Install the salt-minion
    2. Install pytest
    3. Install serverspec
    4. Clone your Salt git repository
    5. Checkout the branch to be tested
    6. Setup salt-minion for masterless mode / local mode

    NOTE: Only supports Ubuntu images at this time

    :param args: A NameSpace object with the arguments required
    :param logging: A python logging object
    :return: An exit code
    """
    logging.info('Instance starting...')
    ec2 = boto3.resource('ec2')
    client = boto3.client('ec2')

    instance = ec2.create_instances(
        ImageId=args.image_id,
        InstanceType=args.instance_type,
        SubnetId=args.subnet_id,
        KeyName=args.keyname,
        SecurityGroupIds=args.security_group_ids.split(','),
        UserData=userdata.OS[args.os].format(git_branch=args.git_branch,
                                             git_repo=args.git_repo,
                                             minion_conf=args.minion_conf,
                                             salt_dir=args.salt_dir),
        MinCount=1,
        MaxCount=1
    )[0]

    while instance.state['Name'] != 'running':
        time.sleep(5)
        instance.reload()
        logging.info('Instance state is {0}...'.format(instance.state['Name']))
    logging.info('Instance started...')

    logging.info('Waiting for Instance status and System status to be in the "ok" state...')
    status = {'InstanceStatus': {'Status': None}, 'SystemStatus': {'Status': None}}
    while status['InstanceStatus']['Status'] != 'ok' and status['SystemStatus']['Status'] != 'ok':
        time.sleep(5)
        status = client.describe_instance_status(InstanceIds=[instance.id])['InstanceStatuses'][0]
        logging.info(
            'Instance status is {0} and '
            'System status is {1}...'.format(status['InstanceStatus']['Status'],
                                             status['SystemStatus']['Status'])
        )

    build_data.write(args.build_id, 'instance', {'id': instance.id,
                                                 'public_ip_address': instance.public_ip_address})
    logging.info('Wrote instance information to build data file...')
    return 0, status, None
