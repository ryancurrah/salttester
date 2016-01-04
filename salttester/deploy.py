import boto3
import time
from salttester import build_data, userdata


def run(args, logging):
    logging.info('Instance starting...')
    ec2 = boto3.resource('ec2')
    instance_id = ec2.create_instances(ImageId=args.image_id,
                                       InstanceType=args.instance_type,
                                       SubnetId=args.subnet_id,
                                       KeyName=args.keyname,
                                       SecurityGroupIds=args.security_group_ids.split(','),
                                       UserData=userdata.OS[args.os].format(git_repo=args.git_repo,
                                                                            git_branch=args.git_branch),
                                       MinCount=1,
                                       MaxCount=1)[0].id

    instance = None
    instance_state = None
    while instance_state != 'running':
        time.sleep(2)
        for instance in ec2.instances.filter(InstanceIds=[instance_id]).all():
            instance_state = instance.state['Name']
            logging.info('Instance state is {0}...'.format(instance_state))
    logging.info('Instance started...')

    build_data.write(args.build_id, 'instance', {'id': instance.id, 'public_ip_address': instance.public_ip_address})
    logging.info('Wrote instance information to build data file...')

    logging.info('Sleeping for 120 seconds...')
    time.sleep(120)
