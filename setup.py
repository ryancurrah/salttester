from distutils.core import setup

setup(
    name='salttester',
    version='0.1',
    packages=['salttester'],
    install_requires=['argparse', 'boto3', 'paramiko'],
    url='www.currah.ca',
    license='Apache',
    author='Ryan Currah',
    author_email='ryan@currah.ca',
    description='SaltStack Test Runner for Py.Test, Highstate and ServerSpec tests Using AWS EC2 and Jenkins '
                'with reports in jUnit',
    keywords='saltstack testing development',
    entry_points={
        'console_scripts': ['salttester=salttester.__main__:main'],
    }
)
