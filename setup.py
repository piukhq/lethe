from setuptools import setup

from version import __version__


setup(
    name='lethe',
    version=__version__,
    description='Forgotten password frontend. Allows users to change their password using a reset token.',
    url='https://git.bink.com/Olympus/lethe',
    author='Chris Latham',
    author_email='cl@bink.com',
    zip_safe=True)
