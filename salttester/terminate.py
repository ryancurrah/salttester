"""
Terminates Deployments
"""
import boto3
from salttester import build_data


def run(args, logging):
    """
    Terminates the AWS EC2 instance

    :param args: A NameSpace object with the arguments required
    :param logging: A python logging object
    :return: An exit code
    """
    instance_id = build_data.read(args.build_id, 'instance', 'id')
    logging.info('Read in config value id="{0}"...'.format(instance_id))

    ec2 = boto3.resource('ec2')
    for instance in ec2.instances.filter(InstanceIds=[instance_id]).all():
        instance.terminate()
    logging.info('Terminated instance "{0}"...'.format(instance_id))
    return 0, 'Terminated instance "{0}"'.format(instance_id), None
