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

- Deploy an Amazon EC2 instance
- Install Salt Minion in standalone/masterless mode
- Add Salt grains
- Run Hightstate and save results as a jUnit report to /tmp/highstate.xml
- Run py.test and save results as a jUnit report to /tmp/pytest.xml
- Run ServerSpec and save results as a jUnit report to /tmp/serverspec.sml
- Downloads jUnit reports into Jenkins job folder
- Terminate an Amazon EC2 instance


Salt-tester requires some work
------------------------------

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

1. Source Code Management > Git > Repository URL

```
https://github.com/ryancurrah/salt-ci-demo.git
```

2. Source Code Management > Git > Branches to build

```
*/master
```

3. Build Environment > Properties Content

```
SALTTESTER_VER=0.4.0
AWS_DEFAULT_REGION=us-east-1
```

4. Build Environment > Inject passwords to the build as environment variables 

```
AWS_ACCESS_KEY_ID=<access_key_id>
AWS_SECRET_ACCESS_KEY=<secret_access_key>
```

5. Build > Virtualenv builder > Python version

```
System-CPython2.7
```

6. Build > Virtualenv builder > Nature

```
Shell
```

7. Build > Virtualenv builder > Command

```
# Install the salttester app
pip install https://github.com/ryancurrah/salttester/blob/master/dist/salttester-$SALTTESTER_VER.tar.gz?raw=true
# Start the instance deployment (synchronous)
salttester -b $BUILD_ID -o ubuntu deploy --image-id ami-d05e75b8 --instance-type t2.micro --keyname tester --git-repo https://github.com/ryancurrah/salt-ci-demo.git --git-branch master --salt-dir /srv/salt --minion-conf /srv/salt/tests/configs/minion --subnet-id subnet-8u447f3 --security-group-ids sg-56b67u
# Run command to set role grain
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

8. Post-build Actions > Publish JUnit test result report > Test report XMLs

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

properties = YAML.load_file('/etc/salt/grains')

set_property properties
```


Example pytest lowstate render test
-----------------------------------

```
import salt.client
caller = salt.client.Caller()


def test_lowstate_render():
    r = caller.cmd('state.show_lowstate')
    assert isinstance(r, list)
    assert len(r) > 0
```


Example pytest pillar render test
---------------------------------

```
import salt.client
caller = salt.client.Caller()


def test_pillar_render():
    r = caller.cmd('pillar.items')
    print r
    assert isinstance(r, dict)
    assert '_errors' not in r
```