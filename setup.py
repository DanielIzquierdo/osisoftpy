# try:
#     from setuptools import setup
# except ImportError:
#     from distutils.core import setup

from setuptools import setup, find_packages

setup(
    name='osisoft_pi_webapi_python_client',
    description='OSIsoft PI Web API client',
    version='1.2.0',
    url='https://gitlab.com/dstcontrols/pge-piclient-python',
    license='MIT',
    author='Andrew Pong <apong@dstcontrols.com>, Alan Kenyon <akenyon@dstcontrols.com>',
    install_requires=[
        'nose',
        'requests',
        'requests-kerberos',
        'rx'
    ],
    # packages=['OSIsoftPy'],
    packages=find_packages(),
    scripts=[],
)
