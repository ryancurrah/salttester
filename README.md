salt-tester
===========

Description
-----------

SaltStack Test Runner for Py.Test, Highstate and ServerSpec tests Using AWS EC2 and Jenkins with reports in jUnit.


This app does the following
---------------------------

- Deploy an Amazon EC2 instance
- Install Salt Minion in standalone/masterless mode
- Add Salt grains
- Run Hightstate and save results as a jUnit report to /tmp/highstate.xml
- Run py.test and save results as a jUnit report to /tmp/pytest.xml
- Run ServerSpec and save results as a jUnit report to /tmp/serverspec.sml
- Downloads jUnit reports into Jenkins job folder
- Terminate an Amazon EC2 instance


This app requires
-----------------

1. Running the salttester app from a Linux Jenkins server with this plugin installed
2. Jenkins server has the jUnit plugin installed
3. Amazon EC2 credential is injected by Jenkins as env variables (http://boto3.readthedocs.org/en/latest/guide/configuration.html#environment-variables) 
4. Minion conf file that specifies the following (See example config below)
    a. Set file_client to 'local'
    b. Set up local file_roots and pillar_roots to your git repo clone directory
5. A minion conf file to use for testing is located in your Salt repo in the tests dir (Eg: tests/configs/minion)
6. ServerSpec spec_helper.rb file imports the yarjuf library to allow for jUnit output (https://github.com/natritmeyer/yarjuf)
7. Include a custom jUnit outputter in your salt states (https://github.com/ryancurrah/salt-ci-demo/blob/master/states/_output/junit.py) 


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
