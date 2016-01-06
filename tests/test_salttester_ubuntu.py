"""
Salttester tests for ubuntu AWS deployer
"""
import logging
import os
from uuid import uuid1
import pytest
import boto3
import salttester

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    level=logging.DEBUG)

BUILD_ID = str(uuid1())

DEPLOY_ARGS = ['-b', BUILD_ID, '-o', 'ubuntu', 'deploy', '--image-id', 'ami-d05e75b8',
               '--instance-type', 't2.micro', '--keyname', 'ryancurrah', '--git-repo',
               'https://github.com/ryancurrah/salt-ci-demo.git', '--git-branch', 'master',
               '--subnet-id', 'subnet-4be20161', '--security-group-ids', 'sg-370eab4e']

GOOD_COMMAND_ARGS = ['-b', BUILD_ID, '-o', 'ubuntu', 'remote', '--port', '22', '--username',
                     'ubuntu', '--key-filename', '/srv/test/test.pem', 'cmd', '--cmd', 'uname -a']

BAD_COMMAND_ARGS = ['-b', BUILD_ID, '-o', 'ubuntu', 'remote', '--port', '22', '--username',
                    'ubuntu', '--key-filename', '/srv/test/test.pem', 'cmd', '--cmd', 'blah -1']

GET_FILE_ARGS = ['-b', BUILD_ID, '-o', 'ubuntu', 'remote', '--port', '22', '--username', 'ubuntu',
                 '--key-filename', '/srv/test/test.pem', 'getfile', '--remote-path', '/etc/hosts',
                 '--local-path', 'testfile.txt']

PYTEST_ARGS = ['-b', BUILD_ID, '-o', 'ubuntu', 'remote', '--port', '22', '--username', 'ubuntu',
               '--key-filename', '/srv/test/test.pem', 'pytest', '--pytest-test-dir',
               '/srv/salt/tests/pytest']

HIGHSTATE_ARGS = ['-b', BUILD_ID, '-o', 'ubuntu', 'remote', '--port', '22', '--username', 'ubuntu',
                  '--key-filename', '/srv/test/test.pem', 'highstate']

TERMINATE_ARGS = ['-b', BUILD_ID, '-o', 'ubuntu', 'terminate']


@pytest.fixture(scope='module')
def ec2_instance(request):
    """
    ec2 instance deploy fixture used to run tests

    :param request: Pytest fixture
    :return: ec2 instance deploy exit code
    """
    parser = salttester.__main__.create_parser()
    # pylint: disable=W0612
    exit_code, stdout, stderr = salttester.deploy.run(parser.parse_args(DEPLOY_ARGS), logging)

    def fin():
        parser = salttester.__main__.create_parser()
        salttester.terminate.run(parser.parse_args(TERMINATE_ARGS), logging)
    request.addfinalizer(fin)
    return exit_code


def test_build_data_db_file_name():
    """
    Test that the db file name is as it expected to be
    """
    assert salttester.build_data.db_file_name('12345') == '12345.db'


def test_build_data_write_read():
    """
    Test that the build_data write function writes a file as expected and
    that the read function finds the correct key and value inputted to the write function
    """
    build_id = uuid1()
    db_file = salttester.build_data.write(build_id, 'instance', {'testkey': 'testvalue'})
    assert os.path.isfile(db_file)
    assert salttester.build_data.read(build_id, 'instance', 'testkey') == 'testvalue'


def test_userdata():
    """
    Test that the userdata inputs are set
    """
    ubuntu = salttester.userdata.OS['ubuntu'].format(git_repo='GIT_REPO', git_branch='GIT_BRANCH')
    assert 'GIT_REPO' in ubuntu and 'GIT_BRANCH' in ubuntu


def test_deploy_ubuntu(ec2_instance):
    """
    Tests that ec2 instance was deployed, there is an instance iid and public ip
    Test that there is an instance with the status running

    :param ec2_instance: Pytest fixture
    """
    assert ec2_instance == 0
    instance_id = salttester.build_data.read(BUILD_ID, 'instance', 'id')
    public_ip_address = salttester.build_data.read(BUILD_ID, 'instance', 'public_ip_address')
    assert isinstance(instance_id, str)
    assert isinstance(public_ip_address, str)
    client = boto3.client('ec2')
    instances = client.describe_instance_status(InstanceIds=[instance_id])['InstanceStatuses']
    assert len(instances) > 0 and instances[0]['InstanceState']['Name'] == 'running'


def test_good_remote_cmd(ec2_instance):
    """
    Tests that ec2 instance was deployed
    Test that remote command execution works and proper result code returned

    :param ec2_instance: Pytest fixture
    """
    assert ec2_instance == 0
    parser = salttester.__main__.create_parser()
    # pylint: disable=W0612
    exit_code, stdout, stderr = salttester.cmd.run(parser.parse_args(GOOD_COMMAND_ARGS), logging)
    assert exit_code == 0
    assert len(stdout) > 0


def test_bad_remote_cmd(ec2_instance):
    """
    Tests that ec2 instance was deployed
    Test that remote command execution fails and proper result code returned

    :param ec2_instance: Pytest fixture
    """
    assert ec2_instance == 0
    parser = salttester.__main__.create_parser()
    # pylint: disable=W0612
    exit_code, stdout, stderr = salttester.cmd.run(parser.parse_args(BAD_COMMAND_ARGS), logging)
    assert exit_code > 0
    assert len(stdout) > 0


def test_get_file_sftp(ec2_instance):
    """
    Tests that ec2 instance was deployed
    Test that remote file download works

    :param ec2_instance: Pytest fixture
    """
    assert ec2_instance == 0
    parser = salttester.__main__.create_parser()
    # pylint: disable=W0612
    exit_code, stdout, stderr = salttester.get_file.run(parser.parse_args(GET_FILE_ARGS), logging)
    assert exit_code == 0
    assert os.path.isfile('testfile.txt')


def test_pystest_tester(ec2_instance):
    """
    Tests that ec2 instance was deployed
    Test that pytest runs successfully

    :param ec2_instance: Pytest fixture
    """
    assert ec2_instance == 0
    parser = salttester.__main__.create_parser()
    # pylint: disable=W0612
    exit_code, stdout, stderr = salttester.pytest.run(parser.parse_args(PYTEST_ARGS), logging)
    assert exit_code == 0
    assert os.path.isfile('pytest.xml')


def test_highstate_tester(ec2_instance):
    """
    Tests that ec2 instance was deployed
    Test that highstate runs successfully

    :param ec2_instance: Pytest fixture
    """
    assert ec2_instance == 0
    parser = salttester.__main__.create_parser()
    # pylint: disable=W0612
    exit_code, stdout, stderr = salttester.highstate.run(parser.parse_args(HIGHSTATE_ARGS), logging)
    assert exit_code == 0
    assert os.path.isfile('highstate.xml')
