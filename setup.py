try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'OSIsoft PI Web API client',
    'author': 'Alan Kenyon',
    'author_email': 'akenyon@dstcontrols.com',
    'version': '0.5.1',
    'install_requires': ['nose'],
    'packages': ['OSIsoftPy'],
    'scripts': [],
    'name': 'OSIsoftPy'
}

setup(**config)
