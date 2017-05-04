# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='osisoftpy',
    description='OSIsoft PI Web WebAPI client',
    version='2.0.0',
    url='https://gitlab.com/dstcontrols/pge-piclient-python',
    license='MIT',
    author='Andrew Pong <apong@dstcontrols.com>',
    install_requires=[
        'requests',
        'requests-kerberos',
        'rx', 'colorlog', 'six', 'arrow', 'pytest'
    ],
    packages=find_packages(),
    scripts=[],
)
