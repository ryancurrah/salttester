salt-tester
===========

Description
-----------
SaltStack Test Runner for Py.Test, Highstate and ServerSpec tests Using AWS EC2 and Jenkins with reports in jUnit.

This app facilitates the following
----------------------------------

- Deploy an Amazon EC2 instance
- Install Salt Minion in standalone mode
- Add Salt grains
- Run py.test and save results as a jUnit report
- Run Hightstate and save results as a jUnit report
- Run ServerSpec and save results as a jUnit report
- Upload jUnit report to Jenkins
- Terminate an Amazon EC2 instance

This app assumes
----------------
- Your running the app from a Linux Jenkins server with Boto3 installed
- Your Amazon EC2 credential is stored in the running users ~/.aws/credentials file or Jenkins injected env variables (http://boto3.readthedocs.org/en/latest/guide/configuration.html#environment-variables) 
- Your Amazon EC2 config is stored in the running users ~/.aws/config file (http://boto3.readthedocs.org/en/latest/guide/configuration.html#environment-variables)