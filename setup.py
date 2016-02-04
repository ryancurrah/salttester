"""
Setup Module
"""
from setuptools import setup

setup(
    name='salttester',
    version='0.4.0',
    packages=['salttester'],
    setup_requires=['pytest-runner'],
    install_requires=['argparse', 'boto3', 'paramiko'],
    tests_require=['pytest', 'pytest-pylint', 'pytest-ordering'],
    url='www.currah.ca',
    license='Apache',
    author='Ryan Currah',
    author_email='ryan@currah.ca',
    description='SaltStack Test Runner for Py.Test, Highstate and ServerSpec tests Using AWS EC2 '
                'and Jenkins with reports in jUnit',
    keywords='saltstack testing development',
    entry_points={
        'console_scripts': ['salttester=salttester.__main__:main'],
    }
)
