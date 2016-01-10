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
 - apt-get install -y python-pip
 - apt-get install -y ruby2.0
 - apt-get install -y salt-minion
 - service salt-minion stop
 - apt-get install -y git
 - git clone {git_repo} /srv/salt
 - git --git-dir=/srv/salt/.git --work-tree=/srv/salt checkout -b {git_branch} origin/{git_branch}
 - cp /srv/salt/tests/configs/minion /etc/salt/minion
 - pip install pytest
 - gem2.0 install serverspec
 - gem2.0 install yarjuf
'''

OS = {'ubuntu': UBUNTU}
