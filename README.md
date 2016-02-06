salt-tester
===========


Description
-----------

SaltStack test executor for Amazon EC2 that has multiple test runners which report test results back in jUnit


Salt-tester test runners
------------------------

1. highstate
2. py.test
3. serverspec


Salt-tester runs on the following operating systems
----------------------------------------------------

1. Ubuntu


Salt-tester allows you to do the following
------------------------------------------

- Deploy Amazon EC2 instance
- Install Salt Minion in standalone/masterless mode
- Run arbitrary commands like adding Grains (Eg: sudeo salt-call grains.append roles apache)
- Run Hightstate and save results as a jUnit report workspace/highstate.xml
- Run Py.Test and save results as a jUnit report to workspace/pytest.xml
- Run ServerSpec and save results as a jUnit report to workspace/serverspec.sml
- Terminate Amazon EC2 instance


Salt-tester requires some changes to your Salt States repo
----------------------------------------------------------
*Example Salt states repo*
https://github.com/ryancurrah/salt-ci-demo

*Minion config for testing*
- Minion conf file to use for testing is located in your Salt repo in a specified dir (Eg: tests/configs/minion)
- Minion conf specifies the following (See example config below)
    a. Set file_client to 'local'
    b. Set up local file_roots and pillar_roots to a local directory

*ServerSpec spec_helper settings*
- ServerSpec spec_helper.rb file imports the yarjuf library to allow for jUnit output (https://github.com/natritmeyer/yarjuf)

*jUnit Salt Outputter*
- Include a custom jUnit outputter in your salt states _outputter dir (https://github.com/ryancurrah/salt-ci-demo/blob/master/states/_output/junit.py) 


Jenkins plugins required
------------------------

1. Git plugin
2. Environment Injector Plugin
3. JUnit Plugin
4. ShiningPanda Plugin


Jenkins setup
-------------

Source Code Management > Git > Repository URL

```
https://github.com/ryancurrah/salt-ci-demo.git
```

Source Code Management > Git > Branches to build

```
*/master
```

Build Environment > Properties Content

```
SALTTESTER_VER=0.4.0
AWS_DEFAULT_REGION=us-east-1
```

Build Environment > Inject passwords to the build as environment variables 

```
AWS_ACCESS_KEY_ID=<access_key_id>
AWS_SECRET_ACCESS_KEY=<secret_access_key>
```

Build > Virtualenv builder > Python version

```
System-CPython2.7
```

Build > Virtualenv builder > Nature

```
Shell
```

Build > Virtualenv builder > Command

```
# Install the salttester app
pip install https://github.com/ryancurrah/salttester/blob/master/dist/salttester-$SALTTESTER_VER.tar.gz?raw=true
# Start the instance deployment (synchronous)
salttester -b $BUILD_ID -o ubuntu deploy --image-id ami-d05e75b8 --instance-type t2.micro --keyname tester --git-repo https://github.com/ryancurrah/salt-ci-demo.git --git-branch master --salt-dir /srv/salt --minion-conf /srv/salt/tests/configs/minion --subnet-id subnet-8u447f3 --security-group-ids sg-56b67u
# Run command to set grains
salttester -b $BUILD_ID -o ubuntu remote --port 22 --username ubuntu --key-filename /var/jenkins_home/tester.pem cmd --cmd "sudo salt-call grains.setval app realcost"
# Run py.test
salttester -b $BUILD_ID -o ubuntu remote --port 22 --username ubuntu --key-filename /var/jenkins_home/tester.pem pytest --pytest-test-dir /srv/salt/tests/pytest
# Start highstate
salttester -b $BUILD_ID -o ubuntu remote --port 22 --username ubuntu --key-filename /var/jenkins_home/tester.pem highstate
# Run serverspec
salttester -b $BUILD_ID -o ubuntu remote --port 22 --username ubuntu --key-filename /var/jenkins_home/tester.pem serverspec --serverspec-test-dir /srv/salt/tests/serverspec/linux
# Terminate instance
salttester -b $BUILD_ID -o ubuntu terminate
```

Post-build Actions > Publish JUnit test result report > Test report XMLs

```
*.xml
```


Example local/masterless minion config
--------------------------------------

```
file_client: local
file_roots:
  base:
    - /srv/salt/states
pillar_roots:
  base:
    - /srv/salt/pillar
```


Example serverspec spec_helper file
-----------------------------------

```
require 'serverspec'
require 'yarjuf'
require 'yaml'

set :backend, :exec

begin
  properties = YAML.load_file('/etc/salt/grains')
rescue Errno::ENOENT 
  properties = Hash.new
end

set_property properties
```


Example pytest lowstate render test
-----------------------------------

```
import salt.client
caller = salt.client.Caller()


def test_lowstate_render():
    s = caller.cmd('state.show_lowstate')
    assert isinstance(s, list)
    assert len(s) > 0
```


Example pytest pillar render test
---------------------------------

```
import salt.client
caller = salt.client.Caller()


def test_pillar_render():
    p = caller.cmd('pillar.items')
    assert isinstance(p, dict)
    assert '_errors' not in p
```