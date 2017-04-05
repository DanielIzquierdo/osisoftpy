# try:
#     from setuptools import setup
# except ImportError:
#     from distutils.core import setup

from setuptools import setup, find_packages

setup(
    name='osisoft-webapi-python-client',
    description='OSIsoft PI Web API client',
    version='1.0.0',
    url='https://gitlab.com/dstcontrols/pge-piclient-python',
    license='MIT',
    author='Andrew Pong',
    author_email='apong@dstcontrols.com',
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
