try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'pyfftviz',
    'author': 'Vincent Khougaz',
    'url': 'https://github.com/sdobz/pyfftviz',
    'download_url': 'https://github.com/sdobz/pyfftviz/archive/master.zip',
    'author_email': 'vincent@khougaz.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['pyfftviz'],
    'scripts': [],
    'name': 'pyfftviz'
}

setup(**config)
