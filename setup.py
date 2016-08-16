try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'OSIsoft PI Web API client',
    'author': 'Alan Kenyon',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'akenyon@dstcontrols.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['PI'],
    'scripts': [],
    'name': 'pipy'
}

setup(**config)
