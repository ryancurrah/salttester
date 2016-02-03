"""
UserData Cloud-Init Instructions
"""

# pylint: disable=C0301
UBUNTU = '''
#cloud-config
repo_update: true

runcmd:
 - wget -O - https://repo.saltstack.com/apt/ubuntu/$(lsb_release -sr)/amd64/latest/SALTSTACK-GPG-KEY.pub | sudo apt-key add -
 - echo "deb http://repo.saltstack.com/apt/ubuntu/$(lsb_release -sr)/amd64/latest $(lsb_release -sc) main" > /etc/apt/sources.list.d/99-saltstack.list
 - apt-get update
 - apt-get install -y git
 - apt-get install -y python-pip
 - apt-get install -y ruby2.0
 - apt-get install -y salt-minion
 - service salt-minion stop
 - git clone -b {git_branch} {git_repo} {salt_dir}
 - cp {minion_conf} /etc/salt/minion
 - pip install pytest
 - gem2.0 install serverspec
 - gem2.0 install yarjuf
'''

OS = {'ubuntu': UBUNTU}
